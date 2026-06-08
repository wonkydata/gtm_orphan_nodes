# Wonkydata.com 
# 
# colab_json_file_upload.py
# 

from google.colab import files
import os

uploaded = files.upload()

for fn in uploaded.keys():
  print(f'User uploaded file "{fn}"')
  # Assuming the user uploads one GTM export JSON file, we'll use the first one.
  # You might need to adjust 'your_gtm_export.json' in the find_hermit_nodes call 
  # below if the uploaded filename is different.
  uploaded_filename = fn

# Now you can use `uploaded_filename` in your function call
# For example, if you uploaded 'GTM-XXXXXX_workspace_export.json',
# you would replace "your_gtm_export.json" with that filename in the next cell's function call.
