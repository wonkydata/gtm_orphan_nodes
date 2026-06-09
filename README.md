# gtm_orphan_nodes

Py script that finds  Orphan nodes (tags, triggers, variables) in an extracted GTM container JSON, and outputs them to copyable text -- so that any GTM user can find and remove orphan elements to reduce container space.

If using Colab, download the code block named "colab_json_file_upload.py" so that Colab can find the file within your environment. 
Otherwise, make sure that the gtm_orphan_nodes.py function runs in an environment that can find your json file(s).

Otherwise run this from any configured IDE. 

Requirement: GTM container JSON(s)
- in Google Tag Manager / Admin for a container, Export Container: this creates the JSON that gtm_orphan_nodes will scan.
- Store the JSON in a file folder for the project where your download of gtm_orphan_nodes.py runs (from your IDE or in Console)
- Edit the gtm_orphan_nodes.py to change the name of the file:
--   In the code snippet (below) in gtm_orphan_nodes.py, edit to the file name of your JSON export file.
--   hermit_tags, hermit_triggers, hermit_variables = find_hermit_nodes("GTM-XXXXXX_workspace999.json")
Caveat: If you're using Colab as your IDE/runtime environment, then download the file "colab_json_file_upload.py". Run this file bebore running gtm_orphan_nodes.py, and it will upload the file to your current Colab notebook.
