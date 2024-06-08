
// This Code is Working Perfectly

var script= document.createElement('script');
script.type='text/javascript';
script.src="https://cdn.tiny.cloud/1//tinymce/5/tinymce.min.js";
script.referrerpolicy="origin"

document.head.appendChild(script);

script.onload=function(){
tinymce.init({
    selector: "#id_content",
    height:656,
    plugins: [
        'advlist autolink preview link image lists charmap print hr anchor pagebreak',
        'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
        'table emoticons template paste help'
      ],
      toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
        'bullist numlist outdent indent | link image | print | media fullpage | ' +
        'forecolor backcolor | ',
      menu: {
        favs: {title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons'}
      },
      menubar: 'favs file edit view insert format tools table help',

    content_css: 'default'

    });
}