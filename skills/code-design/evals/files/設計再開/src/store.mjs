export function createStore(adapter) {
  return {
    save(data) {
      return adapter.write(data);
    },
  };
}
