import {postFormData} from './api'

export async function translateDocument(
  sourceFile,
  outputFilename,
) {
  const formData = new FormData()

  formData.append(
    'file',
    sourceFile,
  )

  formData.append(
    'output_filename',
    outputFilename,
  )

  return await postFormData(
    '/docx/translate',
    formData,
  )
}
