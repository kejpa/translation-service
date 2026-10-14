import {post} from './api'

export async function installModel(model,) {
  return await post('/llm/install-model', model ? {model} : {},)
}
