async function fetchAllCupcakes() {
  const resp = await axios.get('/api/cupcakes')
  return resp.data.cupcakes
}


async function renderCupcakes() {
  const cupcakesList = document.querySelector('#cupcakes-list');
  const cupcakesArr = await fetchAllCupcakes();

  cupcakesArr.forEach( el => {
    const li = document.createElement('li');
    const img = document.createElement('img');
    li.className = 'list-group-item';
    li.innerText = `${el.flavor} - Rating: ${el.rating} - Size: ${el.size}`
    img.src = `${el.image}`
    img.style.height = '150px'
    img.style.display = 'block'
    img.style.margin = '0px auto'
    li.append(img)
    cupcakesList.append(li);
  });
}

renderCupcakes()
