class FormsetRow {
  constructor(formsetInstance, htmlDomElement) {
    this.name = formsetInstance.name
    this.formsetManager = formsetInstance
    this.htmlDomElement = htmlDomElement
    this.htmlButton = this.htmlDomElement.querySelector('.buttonDynamic')
    this.newRow = false
    this.deleted = false
    this.rowId

    // if (
    //   this.formsetManager.parsedInputInitialFormset === 0 ||
    //   parseInt(this.formsetManager.parsedInputTotalFormset) - 1 ===
    //     this.rowId
    // ) {
    //   this.newRow = true
    // }
  }

  getRowId() {
    let getIdRegex = (name) => {
      return name.id.match(/\d+/) // ['0', index: 17, input: 'id_orderline_set-0-id', groups: undefined]
    }

    this.rowId = getIdRegex(
      this.htmlDomElement.querySelector(`input[id^="id_${this.name}_set"]`) // input#id_orderline_set-0-id
    )[0] // '0'

    this.rowId = parseInt(this.rowId)

    return this.rowId
  }

  // removeRow() {
  //   this.deleted = true
  //   // this.formsetManager.handleRowButtons()
  //   this.formsetManager.updateParams('removeRow', this)

  //   if (this.newRow) {
  //     this.htmlDomElement.remove()
  //   } else {
  //     let deleteInputOption = this.htmlDomElement.querySelector(
  //       'input[id$="DELETE"]'
  //     )
  //     deleteInputOption.value = 'on'
  //     this.htmlDomElement.className = 'd-none'
  //   }

  //   this.formsetManager.refreshFormsetRows()
  // }

  insertAfterNode(previousNode, clonedNode) {
    previousNode.parentNode.insertBefore(clonedNode, previousNode.nextSibling)
  }

  addRow() {
    console.log(this, 'inside add row')
    let htmlClonedElement = this.htmlDomElement.cloneNode(true)
    let formsetRegexIds = `${this.name}_set-\\d+` // orderline_set-1-id
    formsetRegexIds = new RegExp(formsetRegexIds, 'g')

    this.formsetManager.updateParams('addRow')

    // Create a new instance of FormsetRow with the new cloned element
    let clonedInstance = new FormsetRow(this.formsetManager, htmlClonedElement)
    clonedInstance.newRow = true
    clonedInstance.rowId = parseInt(
      this.formsetManager.inputTotalFormset.value - 1
    )

    // Update the DOM element with the corresponding ids for the new row
    htmlClonedElement.innerHTML = htmlClonedElement.innerHTML.replaceAll(
      formsetRegexIds,
      `${this.name}_set-${clonedInstance.rowId}`
    )

    // Add the new instance of FormsetRow to the FormsetManager
    this.formsetManager.rows.push(clonedInstance)

    // Insert the cloned element to the DOM
    this.insertAfterNode(this.htmlDomElement, htmlClonedElement)

    // // Refresh buttons
    this.formsetManager.refreshFormsetRows()
  }

  updateRowValue() {
    console.log('updating row value')

    let formsetRegexIds = `${this.name}_set-\\d+` // orderline_set-1-id
    formsetRegexIds = new RegExp(formsetRegexIds, 'g')
    let htmlClonedElement = this.htmlDomElement
    htmlClonedElement.innerHTML = htmlClonedElement.innerHTML.replaceAll(
      formsetRegexIds,
      `${this.name}_set-${this.rowId}`
    )

    this.htmlDomElement.replaceWith(htmlClonedElement)
    console.log(this.htmlDomElement.isConnected, 'sdklajfl')
  }

  handleButton(type) {
    let clonedButton = this.htmlButton.cloneNode(true)

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
      clonedButton.addEventListener('click', () => this.addRow())
    } else if (type === 'removeButton') {
      console.log('configuring remove button')
      clonedButton.textContent = removeButton['content']
      clonedButton.className = removeButton['style']
      this.htmlButton.addEventListener('click', () => this.removeRow())
    }

    this.htmlDomElement.replaceChild(
      clonedButton,
      this.htmlDomElement.querySelector('.dynamicButton')
    )
    // this.htmlButton = clonedButton
    console.log(this.htmlButton.isConnected)
  }
}
class FormsetManager {
  constructor(formsetName) {
    this.name = formsetName
    this.inputTotalFormset
    this.inputInitialFormset
    this.parsedInputInitialFormset
    this.parsedInputTotalFormset
    this.rows = []
    this.newForm = false
    this.loaded = false
    if (this.parsedInputInitialFormset === 0) {
      this.newForm = true
    }
  }

  // handleRowButtons() {
  //   if (this.rows.length > 0) {
  //     this.rows.forEach((row) => {
  //       let row_test = row.getRowId()

  //       if (row_test === this.rows.length - 1) {
  //         row.handleButton('addButton')
  //       } else if (row_test < this.rows.length - 1) {
  //         console.log('handle row button REMOVE')
  //       }
  //     })
  //   }
  // }

  refreshFormsetRows() {
    console.log('refreshing array')
    this.rows.forEach((row) => {
      let rowObject = new FormsetRow(this, row.htmlDomElement)
      console.log(row)
      console.log(rowObject)
      rowObject.rowId = rowObject.getRowId()
      rowObject.updateRowValue()
      console.log(this.rows.length)
      if (rowObject.rowId === this.rows.length - 1) {
        rowObject.handleButton('addButton')
        console.log(rowObject.rowId, this.rows.length, 'hello check')
      } else {
        rowObject.handleButton('removeButton')
        console.log(rowObject.rowId, this.rows.length, 'bye check')
      }
    })

    // if (!this.loaded) {
    //   this.rows = this.rows.filter((object) => {
    //     return object.deleted !== true || object.newRow !== true
    //   })

    //   this.rows.forEach((row) => row.updateRowValue())
    // }

    // this.rows.forEach((row) => {

    //   console.log(row.deleted)
    //   // console.log(row)
    // })
    console.log('end refreshing array')
  }

  getParams() {
    this.inputInitialFormset = document.querySelector(
      `input[name="${formsetName}_set-INITIAL_FORMS"]`
    ) // input#id_orderline_set-INITIAL_FORMS
    this.parsedInputInitialFormset = parseInt(this.inputInitialFormset.value) // 1

    this.inputTotalFormset = document.querySelector(
      `input[name="${formsetName}_set-TOTAL_FORMS"]`
    ) // input#id_orderline_set-TOTAL_FORMS
    this.parsedInputTotalFormset = parseInt(this.inputTotalFormset.value) // 0

    return [this.inputInitialFormset, this.inputTotalFormset]
  }

  updateParams(action, rowObject) {
    if (action === 'addRow') {
      this.inputTotalFormset.value = this.parsedInputTotalFormset + 1
    } else if (action === 'removeRow' && rowObject.newRow) {
      this.inputTotalFormset.value = this.parsedInputTotalFormset - 1
    }
  }
}
// Starting program...
const htmlFormsetDynamicRows = document.querySelectorAll('.formsetDynamic')

const formsetName = 'orderline'
let formsetManager = new FormsetManager(formsetName)
formsetManager.getParams()
htmlFormsetDynamicRows.forEach((htmlFormsetRow, i) => {
  let rowObject = new FormsetRow(formsetManager, htmlFormsetRow)
  rowObject.rowId = rowObject.getRowId()

  if (rowObject.rowId === htmlFormsetDynamicRows.length - 1) {
    rowObject.handleButton('addButton')
  } else if (rowObject.rowId < htmlFormsetDynamicRows.length - 1) {
    rowObject.handleButton('removeButton')
    console.log('handle row button REMOVE')
  }
  formsetManager.rows.push(rowObject)

  console.log('end general for each')
})

// formsetManager.loaded = true
// formsetManager.refreshFormsetRows()
