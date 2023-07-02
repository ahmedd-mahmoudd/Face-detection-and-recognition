
var change= 0;
// Get the input image element
var inputImage = document.getElementById('input-image');

// Add event listener to the input image element
inputImage.addEventListener('change', function() {
    var selectedImage = this.files[0];
    displaySelectedImage(selectedImage, 'input-image-preview');
    change = change + 1;
    showCompareButton();
});

// Get the database image element
var databaseImage = document.getElementById('database-image');

// Add event listener to the database image element
databaseImage.addEventListener('change', function() {
    var selectedImage = this.files[0];
    displaySelectedImage(selectedImage, 'database-image-preview');
    change = change + 1;
    showCompareButton();
});

// Function to display the selected image
function displaySelectedImage(imageFile, previewId) {
    var reader = new FileReader();

    reader.onload = function(event) {
        var preview = document.getElementById(previewId);
        preview.src = event.target.result;
        preview.style.display = 'inline-block';
        preview.style.width = 'auto';
        preview.style.height = '300px';
        preview.style.margin = 'auto';
        preview.style.border = '1px solid white';
        preview.style.borderRadius = '15px' ;
        preview.style['-webkit-box-shadow'] = "4px 8px 19px -3px rgba(0,0,0,0.27)";
        preview.style.boxShadow = '4px 8px 19px -3px rgba(0,0,0,0.27)';

    };

    reader.readAsDataURL(imageFile);
}

// Function to show the Compare button
function showCompareButton() {
    var compareButton = document.getElementById('compare-button');
    if (change == 2) {
    compareButton.style.backgroundColor = '#4CAF50';
    change =0;
    }
}

