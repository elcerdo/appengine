import os
import tempfile

def blob_to_file(filename_hint_propertyname=None,
                 directory_hint=''):
  """Write the blob contents to a file, and replace them with the filename.

  Args:
    filename_hint_propertyname: If present, the filename will begin with
      the contents of this value in the entity being exported.
    directory_hint: If present, the files will be stored in this directory.

  Returns:
    A function which writes the input blob to a file.
  """
  directory = []

  def transform_function(value, bulkload_state):
    if not directory:
      parent_dir = os.path.dirname(bulkload_state.filename)
      directory.append(os.path.join(parent_dir, directory_hint))
      if directory[0] and not os.path.exists(directory[0]):
        os.makedirs(directory[0])

    filename_hint = 'blob_'
    suffix = '.png'
    filename = ''
    if filename_hint_propertyname:
      filename_hint = bulkload_state.current_entity[filename_hint_propertyname]
      filename = os.path.join(directory[0], filename_hint)
      if os.path.exists(filename):
        filename = ''
        (filename_hint, suffix) = os.path.splitext(filename_hint)
    if not filename:
      filename = tempfile.mktemp(suffix, filename_hint, directory[0])
    f = open(filename, 'wb')
    f.write(value)
    f.close()
    return filename

  return transform_function
