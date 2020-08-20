document.querySelector('#createBtn').addEventListener('click', addCupcake)

async function fetchAllCupcakes() {
  const resp = await axios.get('/api/cupcakes')
  return resp.data.cupcakes
}

async function createCupcake(cupcake) {
  try {
    await axios.post('/api/cupcakes', cupcake)
    location.reload();
  }
  catch {
    alert('Cupcake not added')
  }
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

function addCupcake(e) {
  e.preventDefault();
  
  const flavorInput = document.querySelector('#flavor');
  const sizeInput = document.querySelector('#size');
  const ratingInput = document.querySelector('#rating');
  const imageInput = document.querySelector('#image');

  createCupcake({
    flavor: flavorInput.value,
    size: sizeInput.value,
    rating: ratingInput.value,
    image: imageInput.value
  })

  flavorInput.value = '';
  sizeInput.value = '';
  ratingInput.value = '';
  imageInput.value = '';

}

renderCupcakes()
