function main () {
    const input = document.querySelector('#image_input')
    const figureImage = document.querySelector('#preview')

    input.addEventListener('change', (event) => {
        const [file] = event.target.files
        if (file) {
            figureImage.setAttribute('src', URL.createObjectURL(file))
        } 
    })
}
main()