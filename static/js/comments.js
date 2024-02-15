const commentEditButtons = document.getElementsByClassName("btn-edit");
const commentTextElement = document.getElementById("id_body");
const commentEditForm = document.getElementById("comment-form");
const submitButton = document.getElementById("submitButton");

for (let button of commentEditButtons) {
    button.addEventListener("click", (e) => {
        console.log('edit button clicked')
        let commentId = e.target.getAttribute("comment_id");
        let commentContent = document.getElementById(`comment${commentId}`).innerText;
        commentTextElement.value = commentContent;
        submitButton.innerText = "Update";
        commentEditForm.setAttribute("action", `edit_comment/${commentId}`);
    });
}
// not fixed

