const commentEditButtons = document.getElementsByClassName("btn-edit");

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

