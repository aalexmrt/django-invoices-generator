// Create a dynamic button

// Find the container element
const formButtonContainer = document.querySelectorAll('.formButtonContainer')
console.log(formButtonContainer)

formButtonContainer.forEach(function (element) {
  const button = document.createElement('button')
  button.className = 'dynamic-button'
  button.innerHTML = 'Click Me!'
  button.onclick = function () {
    alert('Button clicked!')
  }
  console.log('h3')
  element.appendChild(button)
})

// Append the button to the container

// function getFormParams(form) {
//   const totalFormsInput = document.querySelector(
//     `input[name="${form}_set-TOTAL_FORMS"]`
//   )
//   const initialFormsInput = document.querySelector(
//     `input[name="${form}_set-INITIAL_FORMS"]`
//   )
//   return [totalFormsInput, initialFormsInput]
// }

// function updateFormParams(form) {
//   const [totalFormsInput] = getProductConfigForm(form)
//   totalFormsInput.value = parseInt(totalFormsInput.value) + 1
// }

// function insertAfter(referenceNode, newNode) {
//   referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling)
// }

// function addProductRow(e) {
//   e.preventDefault()
//   console.log('adding new product row')
//   form_row = e.currentTarget.closest('.form-row')
//   // Clone the container div to get a new row
//   new_form_row = form_row.cloneNode(true)
//   // Get the id of the row because I want to increase it
//   old_row_number = new_form_row.querySelector('input').id.match(/\d+/)[0]
//   new_row_number =
//     parseInt(new_form_row.querySelector('input').id.match(/\d+/)[0]) + 1
//   form_regex = /product_set-\d+/g
//   // Update the row with the corresponding ids
//   new_form_row.innerHTML = new_form_row.innerHTML.replaceAll(
//     form_regex,
//     `product_set-${new_row_number}`
//   )
//   // Conver the previous button to a remove button
//   button = form_row.querySelector('button')
//   button.classList.remove('bg-green-500', 'hover:bg-green-700', 'add-form-row')
//   button.classList.add('bg-red-500', 'hover:bg-red-700', 'remove-form-row')
//   button.innerHTML = '-'
//   button.removeEventListener('click', addProductRow)

//   insertAfter(form_row, new_form_row)
//   updateButtons()
//   updateFormParams('orderline')
// }

// function removeProductRow(e) {
//   e.preventDefault()
//   form_row = e.currentTarget.closest('.form-row')
//   form_row.style.display = 'none'
//   // Get the input which id ends with DELETE
//   delete_row = form_row.querySelector('input[id$="DELETE"]')
//   // Mark the row with value on to delete this row in the view
//   delete_row.value = 'on'

//   updateButtons()
// }

// function updateButtons() {
//   remove_button = document.querySelectorAll('.remove-form-row')
//   remove_button.forEach((btn) =>
//     btn.addEventListener('click', removeProductRow)
//   )

//   add_button = document.querySelector('.add-form-row')
//   add_button.addEventListener('click', addProductRow)
// }

// updateButtons()
// getFormParams('orderline')
