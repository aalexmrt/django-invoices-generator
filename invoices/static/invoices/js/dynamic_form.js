// Create a dynamic button

// Find the container element
const formButtonContainer = document.querySelectorAll('.formButtonContainer')
console.log(formButtonContainer)
const button = []
formButtonContainer.forEach(function (element) {
  button = document.createElement('button')
  button.className = 'dynamic-button'
  button.innerHTML = 'Click Me!'
  button.onclick = function () {
    alert('Button clicked!')
  }
  console.log('h3')
  element.appendChild(button)
})
