// v.0.0.3
// Starting program...
const FormsetManager = {
  formsetName: 'orderline',
  inputInitialFormset: null,
  inputTotalFormset: null,
  htmlFormsetDynamicRows: null,

  initialize() {
    this.inputInitialFormset = this.getInput('INITIAL_FORMS')
    this.inputTotalFormset = this.getInput('TOTAL_FORMS')
    this.htmlFormsetDynamicRows = $('.formsetDynamic')

    this.bindButtons()
  },

  getInput(inputName) {
    return $(`input[name="${this.formsetName}_set-${inputName}"]`)
  },

  getRowId(htmlDomElement) {
    const rowId = htmlDomElement
      .find(`input[id^="id_${this.formsetName}_set"]`)
      .attr('id')
      .match(/\d+/)[0]
    return parseInt(rowId)
  },

  insertAfterNode(previousNode, clonedNode) {
    $(previousNode).after(clonedNode)
  },

  addRow(htmlFormsetRow, button) {
    const htmlClonedElement = htmlFormsetRow.clone()
    const formsetRegexIds = `${this.formsetName}_set-\\d+`
    const newRowId = this.htmlFormsetDynamicRows.length

    htmlClonedElement.html(
      htmlClonedElement
        .html()
        .replace(
          new RegExp(formsetRegexIds, 'g'),
          `${this.formsetName}_set-${newRowId}`
        )
    )

    button.addClass('d-none')
    this.insertAfterNode(htmlFormsetRow, htmlClonedElement)
  },

  handleButton(button, type, htmlFormsetRow) {
    const addButton = {
      content: '+',
      style: 'btn btn-outline-success buttonDynamic',
    }

    let clonedButton = button.clone()

    if (type === 'addButton') {
      clonedButton.text(addButton.content).addClass(addButton.style)
      clonedButton.on('click', () => this.addRow(htmlFormsetRow, clonedButton))
    } else {
      clonedButton.text('').addClass('d-none')
    }

    button.replaceWith(clonedButton)
    return clonedButton
  },

  bindButtons() {
    this.htmlFormsetDynamicRows.each((index, htmlFormsetRow) => {
      const button = $(htmlFormsetRow).find('.buttonDynamic')

      if (index === this.htmlFormsetDynamicRows.length - 1) {
        this.handleButton(button, 'addButton', htmlFormsetRow)
      } else {
        this.handleButton(button, '', htmlFormsetRow)
      }
    })
  },
}

$(document).ready(() => {
  FormsetManager.initialize()
})
