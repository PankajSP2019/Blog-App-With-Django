//This file is created by - Pankaj Kumar Das
//The purpose of this file is to Inject Js in the Django Admin Panel
//For using TinyMCE Editor, edit the Blog


// This Code is Not Working

//var script = document.CreateElement('script');
//script.type = 'text/javascript';
//script.src = "https://cdn.tiny.cloud/1/no-api-key/tinymce/7/tinymce.min.js";
//document.head.appendChild(script);
//script.onload = function(){
//    tinymce.init({
//            selector: '#id_content',
//            height:500,
//            plugins: 'anchor preview autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage advtemplate mentions tableofcontents footnotes mergetags autocorrect typography inlinecss markdown code',
//            toolbar: 'undo redo | preview | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
//            menu: {
//                code: { title: 'Code', items: 'code' },
//                edit: { title: 'Edit', items: 'undo, redo, selectall' }
//            },
//            menubar: 'file edit view insert tools table code'
//
//        });
//}


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
        'advlist autolink link image lists charmap print hr anchor pagebreak',
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