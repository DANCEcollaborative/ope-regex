import nbformat as nbf

def is_task_n(task: str):
  def is_target_task(cell):
    if not 'tags' in cell['metadata'].keys():
      return False
    if len(cell['metadata']['tags']) <= 0:
      return False
    return cell['cell_type'] == 'code' and cell['metadata']['tags'][0] == task
  return is_target_task

def extract_task_n_code(nbPath:str, taskTag: str) -> str:
  lines = []
  is_target_task = is_task_n(taskTag)
  with open(nbPath) as f:
    nb = nbf.read(f, as_version=4)
    for cell in nb.cells:
      if is_target_task(cell):
        lines.append(cell['source'])
  code = '\n'.join(lines)
  return code

def string_to_function(code: str, funcName: str):
  local_vars = {}
  exec(code, local_vars)
  fn = local_vars[funcName]
  return fn

def release(task: str):
  source_path = f'./tasks/{task}.ipynb'
  target_path = './workspace/workspace.ipynb'
  # Load the source notebook
  with open(source_path) as f:
    source_nb = nbf.read(f, as_version=4)

  # Load the target notebook
  with open(target_path) as f:
    target_nb = nbf.read(f, as_version=4)

  # Append cells of the source notebook to the target
  target_nb.cells.extend(source_nb.cells)

  # Write the combined notebook back to the first file
  with open(target_path, 'w') as f:
    nbf.write(target_nb, f)