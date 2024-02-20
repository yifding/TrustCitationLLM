import pandas as pd


input_file = '/var/www/html/trust/trust/result.jsonl'
df = pd.read_json(input_file, lines=True)