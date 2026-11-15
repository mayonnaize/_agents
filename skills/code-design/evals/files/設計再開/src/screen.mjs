export async function onSave(store, readInput, showMessage) {
  const result = await store.save(readInput());
  showMessage("保存しました");
  return result;
}
