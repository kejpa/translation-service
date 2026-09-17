import {postFormData} from './api'

export async function importDocumentPair(
  sourceFile,
  targetFile,
) {
  const formData = new FormData()

  formData.append(
    'source_file',
    sourceFile,
  )

  formData.append(
    'target_file',
    targetFile,
  )

  return await postFormData(
    '/document-pairs/import',
    formData,
  )
}
