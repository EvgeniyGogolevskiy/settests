function radioSelect(node) {
    const quest_id = document.getElementById('quest_id');
    sessionStorage.setItem(quest_id.value, node.value);
    const answerKey = sessionStorage.getItem(quest_id.value);
}


function buttontConfirm() {
    const btn_finish = document.getElementById('btn_finish');
    let keys = Object.keys(sessionStorage);
    let s = '';
    for(let key of keys) {
        s =  sessionStorage.getItem(key) + ',' + s ;
    }
    btn_finish.value = s;
    sessionStorage.clear();
}


