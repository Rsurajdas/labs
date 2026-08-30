function twoSumEarliest(values, target) {
  // TODO
  const hashMap = {};
  const output = [];
  for (let i = 0; i < values.length; i++) {
    const need = target - values[i];
    console.log({ need });
    if (!Object.values(hashMap).includes(need)) {
      hashMap[i] = need;
    }
  }
  return hashMap;
}

console.log(twoSumEarliest([2, 7, 11, 5], 9));
