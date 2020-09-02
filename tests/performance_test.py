import os
import sys
import talon
import pandas as pd
talon.init()
from talon import signature

kwargs = {}
if sys.version_info > (3, 0):
    kwargs["encoding"] = "utf8"
test_folder = '/Users/henrywinn/workspace/forge/dataset/split_emails'

def get_accuracy_stats(annotated_email, extracted_df=None):
    results = {
        'tp': 0,
        'tn': 0,
        'fp': 0,
        'fn': 0
    }
    test_without_annotations = annotated_email.replace('#sig#', '')
    split = annotated_email.split('#sig#', 1)
    true_body = split[0]
    if len(split) > 1:
        true_sig = split[1].replace('#sig#', '')
    else:
        true_sig = ''
    text, sig = signature.extract(test_without_annotations)
    if extracted_df is not None:
        extracted_df = extracted_df.append([{'raw':annotated_email, 'body':text, 'sig':sig}])
    if len(true_body.splitlines()) > len(text.splitlines()): #if extractor took off too much
        results['fp'] += len(true_body.splitlines()) - len(text.splitlines())
        results['tn'] += len(text.splitlines())
        results['tp'] += len(true_sig.splitlines())
    elif len(true_body.splitlines()) < len(text.splitlines()): #extractor took off too little
        results['fn'] += len(true_sig.splitlines())
        results['tn'] += len(true_body.splitlines())
        if sig is not None:
            results['tp'] += len(sig.splitlines())
    else:
        results['tp'] += len(true_sig.splitlines())
        results['tn'] += len(true_body.splitlines())
    return results, extracted_df

def merge_results(r1, r2):
    return {
        'tp': r1['tp'] + r2['tp'],
        'tn': r1['tn'] + r2['tn'],
        'fp': r1['fp'] + r2['fp'],
        'fn': r1['fn'] + r2['fn']
    }

results = {
        'tp': 0,
        'tn': 0,
        'fp': 0,
        'fn': 0
    }
df = pd.DataFrame(columns=['raw','body','sig'])
for filename in [f for f in os.listdir(test_folder) if not f.startswith('.')]:
    filename = os.path.join(test_folder, filename)
    with open(filename, **kwargs) as f:
        msg = f.read()
        msg_results, df = get_accuracy_stats(msg, extracted_df=df)
        results = merge_results(results, msg_results)

print('swag')