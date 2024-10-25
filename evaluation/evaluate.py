from pathlib import Path

import numpy as np
import pandas as pd
import boto3
from tempfile import NamedTemporaryFile
import json

from epilepsy2bids.annotations import Annotations, SeizureType
from timescoring import annotations, scoring

FS = 256


def toMask(annotations):
    mask = np.zeros(int(annotations.events[0]["recordingDuration"] * FS))
    for event in annotations.events:
        if event["eventType"].value != "bckg":
            mask[
                round(event["onset"] * FS): round(event["onset"] + event["duration"])
                * FS
            ] = 1
    return mask


def computeScores(tp, fp, refTrue, duration):
    # Sensitivity
    if refTrue > 0:
        sensitivity = tp / refTrue
    else:
        sensitivity = np.nan  # no ref event

    # Precision
    if tp + fp > 0:
        precision = tp / (tp + fp)
    else:
        precision = np.nan  # no hyp event

    # F1 Score
    if np.isnan(sensitivity) or np.isnan(precision):
        f1 = np.nan
    elif (sensitivity + precision) == 0:  # No overlap ref & hyp
        f1 = 0
    else:
        f1 = 2 * sensitivity * precision / (sensitivity + precision)

    # FP Rate
    fpRate = fp / (duration / 3600 / 24)  # FP per day

    return sensitivity, precision, f1, fpRate


def evaluate(refFolder: str, hypFolder: str):
    DATASET = "tuh"
    results = {
        "dataset": [],
        "subject": [],
        "file": [],
        "duration": [],
        "tp_sample": [],
        "fp_sample": [],
        "refTrue_sample": [],
        "tp_event": [],
        "fp_event": [],
        "refTrue_event": [],
    }
    for refTsv in Path(refFolder).glob("sub-*/**/*.tsv"):
        ref = Annotations.loadTsv(refTsv)
        ref = annotations.Annotation(toMask(ref), FS)
        hypTsv = Path(hypFolder) / refTsv.relative_to(refFolder)
        if hypTsv.exists():
            hyp = Annotations.loadTsv(hypTsv)
            hyp = annotations.Annotation(toMask(hyp), FS)
        else:
            hyp = annotations.Annotation(np.zeros_like(ref.mask), ref.fs)

        sampleScore = scoring.SampleScoring(ref, hyp)
        eventScore = scoring.EventScoring(ref, hyp)

        results["dataset"].append(DATASET)
        results["subject"].append(refTsv.name.split("_")[0])
        results["file"].append(refTsv.name)
        results["duration"].append(len(ref.mask) / ref.fs)
        results["tp_sample"].append(sampleScore.tp)
        results["fp_sample"].append(sampleScore.fp)
        results["refTrue_sample"].append(sampleScore.refTrue)
        results["tp_event"].append(eventScore.tp)
        results["fp_event"].append(eventScore.fp)
        results["refTrue_event"].append(eventScore.refTrue)

    results = pd.DataFrame(results)

    results.to_csv("results.csv")

    # Sample results
    sensitivity, precision, f1, fpRate = computeScores(
        results["tp_sample"].sum(),
        results["fp_sample"].sum(),
        results["refTrue_sample"].sum(),
        results["duration"].sum(),
    )
    print(
        "# Sample scoring\n"
        + "- Sensitivity : {:.2f} \n".format(sensitivity)
        + "- Precision   : {:.2f} \n".format(precision)
        + "- F1-score    : {:.2f} \n".format(f1)
        + "- FP/24h      : {:.2f} \n".format(fpRate)
    )

    # Event results
    sensitivity, precision, f1, fpRate = computeScores(
        results["tp_event"].sum(),
        results["fp_event"].sum(),
        results["refTrue_event"].sum(),
        results["duration"].sum(),
    )
    print(
        "# Event scoring\n"
        + "- Sensitivity : {:.2f} \n".format(sensitivity)
        + "- Precision   : {:.2f} \n".format(precision)
        + "- F1-score    : {:.2f} \n".format(f1)
        + "- FP/24h      : {:.2f} \n".format(fpRate)
    )


def evaluate_s3(AWS_REGION: str, AWS_BUCKET: str, AWS_ACCESS_KEY: str, AWS_SECRET_KEY: str):

    results = {
        "dataset": [],
        "subject": [],
        "file": [],
        "duration": [],
        "tp_sample": [],
        "fp_sample": [],
        "refTrue_sample": [],
        "tp_event": [],
        "fp_event": [],
        "refTrue_event": [],
    }

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
    # List objects in the bucket
    
    response = s3.list_objects_v2(Bucket=AWS_BUCKET)
    count = 0

    for obj in response.get('Contents', []):
        file_path = obj['Key']

        if file_path.endswith('.tsv') and not file_path.endswith('participants.tsv') and file_path.startswith('datasets/'):
            refTsv = file_path
            DATASET = refTsv.split('/')[1]

            # Get the object from S3
            tsv_content = s3.get_object(Bucket=AWS_BUCKET, Key=refTsv)

#           Read the content of the file
            tsv_obj = tsv_content['Body'].read().decode('utf-8')

            # Write the content to a temporary file (we can remove this later once library is updated)
            with NamedTemporaryFile(delete=False, mode='w', suffix='.tsv') as temp_file:
                temp_file.write(tsv_obj)
                temp_file_path = temp_file.name

            ref = Annotations.loadTsv(temp_file_path)
            ref = annotations.Annotation(toMask(ref), FS)
            print(refTsv, "\nRef Annotation: ", ref)

            # Get the corresponding hypothesis file from the algo1 folder
            # hypTsv_base = 'submission/algo1/'
            # hypTsv = hypTsv_base + refTsv.replace("datasets/", "", 1)
            # print(hypTsv)
            # hyp_tsv_content = s3.get_object(Bucket=AWS_BUCKET, Key=hypTsv)
            # print(hypTsv, hyp_tsv_content)

            hypTsv = temp_file_path

            if hypTsv:
                hyp = Annotations.loadTsv(hypTsv)
                hyp = annotations.Annotation(toMask(hyp), FS)
            else:
                hyp = annotations.Annotation(np.zeros_like(ref.mask), ref.fs)

            sampleScore = scoring.SampleScoring(ref, hyp)
            eventScore = scoring.EventScoring(ref, hyp)

            # results["dataset"].append(DATASET)

            # dataset logic for testing
            if count > 250:
                DATASET = 'group2'
            results["dataset"].append(DATASET)

            results["subject"].append(refTsv.split("/")[2])
            results["file"].append(refTsv.split("/")[-1])

            results["duration"].append(len(ref.mask) / ref.fs)
            results["tp_sample"].append(sampleScore.tp)
            results["fp_sample"].append(sampleScore.fp)
            results["refTrue_sample"].append(sampleScore.refTrue)
            results["tp_event"].append(eventScore.tp)
            results["fp_event"].append(eventScore.fp)
            results["refTrue_event"].append(eventScore.refTrue)
            count += 2
            if count > 500:
                break

            print(count)

    results = pd.DataFrame(results)
    grouped_results = results.groupby('dataset')[
        ['tp_sample', 'fp_sample', 'refTrue_sample', 'duration']].sum().reset_index()
    print(grouped_results.head())

    results.to_csv("results.csv")

    result_dict = {
        "algo_id": "ANN",
        "datasets": []
    }
    # Sample results
    for dataset in results['dataset'].unique():
        temp = {}
        dataset_results = results[results['dataset'] == dataset]
        sensitivity_sample, precision_sample, f1_sample, fpRate_sample = computeScores(
            dataset_results["tp_sample"].sum(),
            dataset_results["fp_sample"].sum(),
            dataset_results["refTrue_sample"].sum(),
            dataset_results["duration"].sum(),)

        sensitivity_event, precision_event, f1_event, fpRate_event = computeScores(
            dataset_results["tp_event"].sum(),
            dataset_results["fp_event"].sum(),
            dataset_results["refTrue_event"].sum(),
            dataset_results["duration"].sum())

        temp["dataset"] = dataset

        temp["sample_results"] = {}
        temp["sample_results"]["sensitivity"] = sensitivity_sample
        temp["sample_results"]["precision"] = precision_sample
        temp["sample_results"]["f1"] = f1_sample
        temp["sample_results"]["fpRate"] = fpRate_sample

        temp["event_results"] = {}
        temp["event_results"]["sensitivity"] = sensitivity_event
        temp["event_results"]["precision"] = precision_event
        temp["event_results"]["f1"] = f1_event
        temp["event_results"]["fpRate"] = fpRate_event

        result_dict['datasets'].append(temp)

    # Convert result_dict to JSON
    json_object = json.dumps(result_dict)
    
    # Print JSON object
    print(json_object)
    
    # Write JSON object to S3
    s3.put_object(Bucket=AWS_BUCKET, Key='results/results.json', Body=json_object)
    
    # Write results.csv to S3
    with open("results.csv", "rb") as csv_file:
        s3.put_object(Bucket=AWS_BUCKET, Key='results/results.csv', Body=csv_file)

