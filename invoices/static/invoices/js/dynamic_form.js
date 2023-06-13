// v.0.0.1

// Starting program...

function getParams(formsetName) {
  let inputInitialFormset = document.querySelector(
    `input[name="${formsetName}_set-INITIAL_FORMS"]`
  ) // input#id_orderline_set-INITIAL_FORMS

  let inputTotalFormset = document.querySelector(
    `input[name="${formsetName}_set-TOTAL_FORMS"]`
  ) // input#id_orderline_set-TOTAL_FORMS

  return [inputInitialFormset, inputTotalFormset]
}

function getRowId(formsetName, htmlDomElement) {
  let getIdRegex = (name) => {
    return name.id.match(/\d+/) // ['0', index: 17, input: 'id_orderline_set-0-id', groups: undefined]
  }

  let rowId = getIdRegex(
    htmlDomElement.querySelector(`input[id^="id_${formsetName}_set"]`) // input#id_orderline_set-0-id
  )[0] // '0'

  rowId = parseInt(rowId)

  return rowId
}

function insertAfterNode(previousNode, clonedNode) {
  previousNode.parentNode.insertBefore(clonedNode, previousNode.nextSibling)
}
function addRow(htmlFormsetRow, button) {
  let htmlClonedElement = htmlFormsetRow.cloneNode(true)
  let formsetRegexIds = `${formsetName}_set-\\d+` // orderline_set-1-id
  formsetRegexIds = new RegExp(formsetRegexIds, 'g')

  inputTotalFormset.value = parseInt(inputTotalFormset.value) + 1
  let newRowId = parseInt(inputTotalFormset.value) - 1
  // Update the DOM element with the corresponding ids for the new row
  htmlClonedElement.innerHTML = htmlClonedElement.innerHTML.replaceAll(
    formsetRegexIds,
    `${formsetName}_set-${newRowId}`
  )

  button.className = 'd-none'
  // Insert the cloned element to the DOM
  let newButton = htmlClonedElement.querySelector('.buttonDynamic')
  newButton = handleButton(newButton, 'addButton', htmlClonedElement)
  insertAfterNode(htmlFormsetRow, htmlClonedElement)
}

function handleButton(button, type, htmlFormsetRow) {
  let clonedButton = button.cloneNode(true)

  const addButton = {
    content: '+',
    style: 'btn btn-outline-success buttonDynamic',
  }
  const removeButton = {
    content: '-',
    style: 'btn btn-outline-danger buttonDynamic',
  }

  if (type === 'addButton') {
    clonedButton.textContent = addButton.content
    clonedButton.className = addButton.style
    clonedButton.addEventListener('click', () =>
      addRow(htmlFormsetRow, clonedButton)
    )
  } else if (type === 'removeButton') {
    clonedButton.textContent = removeButton['content']
    clonedButton.className = removeButton['style']
    this.htmlButton.addEventListener('click', () => removeRow())
  } else {
    clonedButton.textContent = ''
    clonedButton.className = 'd-none'
  }

  button.replaceWith(clonedButton)

  return clonedButton
}

const htmlFormsetDynamicRows = document.querySelectorAll('.formsetDynamic')

const formsetName = 'orderline'

let [inputInitialFormset, inputTotalFormset] = getParams(formsetName)

htmlFormsetDynamicRows.forEach((htmlFormsetRow) => {
  let rowId = getRowId(formsetName, htmlFormsetRow)
  console.log(rowId)
  let button = htmlFormsetRow.querySelector('.buttonDynamic')

  if (rowId === htmlFormsetDynamicRows.length - 1) {
    button = handleButton(button, 'addButton', htmlFormsetRow)
  } else {
    button = handleButton(button, '', htmlFormsetRow)
  }
})
