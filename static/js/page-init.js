function setNav() {
    var rootPath;
    var curWwwPath = window.document.location.href;
    var pathName = window.document.location.pathname;
    var pos = curWwwPath.indexOf(pathName);
    rootPath = curWwwPath.substring(0, pos);
    $('.navbar-brand').attr('href', rootPath);
    $('#nav_animal').attr('href', rootPath + '/AnimalRec');
}
