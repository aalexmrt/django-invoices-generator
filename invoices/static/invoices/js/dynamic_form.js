// v.0.0.2
// Starting program...

function getParams(formsetName) {
  // input#id_orderline_set-INITIAL_FORMS
  let inputInitialFormset = $(`input[name="${formsetName}_set-INITIAL_FORMS"]`)

  // input#id_orderline_set-TOTAL_FORMS
  let inputTotalFormset = $(`input[name="${formsetName}_set-TOTAL_FORMS"]`)

  return [inputInitialFormset, inputTotalFormset]
}

function getRowId(formsetName, htmlDomElement) {
  let getIdRegex = (name) => {
    // ['0', index: 17, input: 'id_orderline_set-0-id', groups: undefined]
    return name.id.match(/\d+/)
  }

  let rowId = getIdRegex(
    // input#id_orderline_set-0-id
    htmlDomElement.$(`input[id^="id_${formsetName}_set"]`)
  )[0] // '0'

  rowId = parseInt(rowId)
  return rowId
}

function insertAfterNode(previousNode, clonedNode) {
  $(previousNode).after(clonedNode)
}

function addRow(htmlFormsetRow, button) {
  let htmlClonedElement = htmlFormsetRow.clone()
  let formsetRegexIds = `${formsetName}_set-\\d+` // orderline_set-1-id
  formsetRegexIds = new RegExp(formsetRegexIds, 'g')

  inputTotalFormset.value = parseInt(inputTotalFormset.val()) + 1
  let newRowId = parseInt(inputTotalFormset.val()) - 1
  // Update the DOM element with the corresponding ids for the new row
  $(htmlClonedElement).html(
    $(htmlClonedElement)
      .html()
      .replaceAll(formsetRegexIds, `${formsetName}_set-${newRowId}`)
  )

  button.addClass('d-none')
  // Insert the cloned element to the DOM
  let newButton = htmlClonedElement.$('.buttonDynamic')
  newButton = handleButton(newButton, 'addButton', htmlClonedElement)
  insertAfterNode(htmlFormsetRow, htmlClonedElement)
}

function handleButton(button, type, htmlFormsetRow) {
  let clonedButton = button.clone()

  const addButton = {
    content: '+',
    style: 'btn btn-outline-success buttonDynamic',
  }
  //this functionality is not implemented yet
  // const removeButton = {
  //   content: '-',
  //   style: 'btn btn-outline-danger buttonDynamic',
  // }

  if (type === 'addButton') {
    clonedButton.text(addButton.content)
    clonedButton.addClass(addButton.style)
    clonedButton.click(() => addRow(htmlFormsetRow, clonedButton))
    // this functionality is not implemented yet
    // } else if (type === 'removeButton') {
    //   clonedButton.textContent = removeButton['content']
    //   clonedButton.className = removeButton['style']
    //   this.htmlButton.addEventListener('click', () => removeRow())
    // }
  } else {
    clonedButton.text('')
    clonedButton.addClass('d-none')
  }

  button.replaceWith(clonedButton)

  return clonedButton
}

const htmlFormsetDynamicRows = document.$('.formsetDynamic')
const formsetName = 'orderline'
let [inputInitialFormset, inputTotalFormset] = getParams(formsetName)

htmlFormsetDynamicRows.each((htmlFormsetRow) => {
  let rowId = getRowId(formsetName, htmlFormsetRow)
  let button = htmlFormsetRow.$('.buttonDynamic')

  if (rowId === htmlFormsetDynamicRows.length - 1) {
    button = handleButton(button, 'addButton', htmlFormsetRow)
  } else {
    button = handleButton(button, '', htmlFormsetRow)
  }
})
