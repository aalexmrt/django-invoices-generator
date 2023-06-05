const formsetName = 'orderline'
const inputTotalFormset = document.querySelector(
  `input[name="${formsetName}_set-TOTAL_FORMS"]`
)
const inputInitialFormset = document.querySelector(
  `input[name="${formsetName}_set-INITIAL_FORMS"]`
)

let inputLastRowValue = parseInt(inputTotalFormset.value) - 1

class FormsetManager {
  constructor(formsetName, domElement) {
    this.name = formsetName
    this.domElement = domElement
    this.button = this.domElement.querySelector('.buttonDynamic')
    this.isLastRow = false
    this.currentRowValue

    this.handleButton()
  }

  getIdRegex(name) {
    return name.id.match(/\d+/)
  }

  getParams() {
    this.currentRowValue = this.getIdRegex(
      this.domElement.querySelector(`input[id^="id_${this.name}_set"]`)
    )[0]
    console.log(
      this.currentRowValue,
      'this is the current row value when performing get params'
    )
  }

  updateParams(action) {
    let parsedInputTotalFormsetValue = parseInt(inputTotalFormset.value)
    if (action === 'addRow') {
      console.log('updating input last row value')
      inputTotalFormset.value = parsedInputTotalFormsetValue + 1
      inputLastRowValue += 1
    } else if (action === 'removeRow') {
      inputTotalFormset.value = parsedInputTotalFormsetValue - 1
      inputLastRowValue -= 1
    }
  }

  removeRow() {
    let deleteInputOption = this.domElement.querySelector('input[id$="DELETE"]')
    deleteInputOption.value = 'on'

    this.domElement.className = 'd-none'
    this.updateParams('addRow')
    this.handleButton()
  }

  insertAfterNode(previousNode, clonedNode) {
    previousNode.parentNode.insertBefore(clonedNode, previousNode.nextSibling)
  }

  addRow() {
    let clonedDomElement = this.domElement.cloneNode(true)
    let inputNewRowValue = inputLastRowValue + 1

    let formsetRegexIds = `${this.name}_set-\\d+` // orderline_set-1-id
    formsetRegexIds = new RegExp(formsetRegexIds, 'g')

    // Update the row with the corresponding ids
    clonedDomElement.innerHTML = clonedDomElement.innerHTML.replaceAll(
      formsetRegexIds,
      `${this.name}_set-${inputNewRowValue}`
    )
    this.updateParams('addRow')
    let cloneInstance = new FormsetManager(this.name, clonedDomElement)
    this.insertAfterNode(this.domElement, clonedDomElement)
    this.handleButton()

    return cloneInstance
  }

  handleButton() {
    this.getParams()
    const addButton = {
      content: '+',
      style: 'btn btn-outline-success buttonDynamic',
      callback: () => {
        this.addRow()
      },
    }
    const removeButton = {
      content: '-',
      style: 'btn btn-outline-danger buttonDynamic',
      callback: () => {
        this.removeRow()

        // // this.removeRow()
      },
    }

    // Add a button to add a new row but only in last row of the formset and remove buttons to the other rows if exists
    if (this.currentRowValue == inputTotalFormset.value - 1) {
      this.isLastRow = true
      this.button.textContent = addButton.content
      this.button.className = addButton.style
      this.button.addEventListener('click', addButton.callback)
    } else {
      this.isLastRow = false
      this.button.textContent = removeButton['content']
      this.button.className = removeButton['style']
      this.button.addEventListener('click', removeButton.callback)
    }
  }
}
const formsetDynamic = document.querySelectorAll('.formsetDynamic')

formsetDynamic.forEach((container, index) => {
  const formsetRow = new FormsetManager(formsetName, container)
  // const button = document.querySelector('.buttonDynamic')
  // let dynamicButton = new DynamicButton(button)
  // index === formDynamic.length - 1
  //   ? dynamicButton.configureAddButton((e) => {
  //       addFormsetRow(e, 'orderline')
  //     })
  //   : console.log('hello')
})

// formButtonContainer.forEach((container, index) => {
//   const button = (index === formButtonContainer.length - 1)
//     ? dynamicButton.createAddButton((e) => {
//         e.preventDefault();
//         alert('hello');
//       })
//     : dynamicButton.createRemoveButton((e) => {
//         e.preventDefault();
//         alert('hello');
//       });

//   container.appendChild(button);
