console.log("test")

async function getForums() {
    return fetch("get_forum/").then((res) => res.json())
}

async function refreshForums() {
    document.getElementById("list_of_forms").innerHTML = ""
    const Forums = await getForums()
    // Access the userRole data attribute
    var userRoleElement = document.getElementById("userRole");
    var userRole = userRoleElement.getAttribute("data-role");

    // Now, you can use the userRole variable in your JavaScript
    console.log("User Role:", userRole);

    let htmlString =``;

    // Add the "DEBUG" header only when userRole is 'A'
    if (Forums.length > 0) {
        document.getElementById("forumHead").innerHTML = "<h2>Forum Discussion</h2>";
    } else {
        document.getElementById("forumHead").innerHTML = "<h2>There's no forum yet</h2>";
    }

    htmlString += `</tr>`;
    
    Forums.forEach((forum) => {
        console.log(forum);

        htmlString += `
            <tr class="TableContent" >
                <td onclick="window.location='forum/${forum.pk}/';" class="col-md-9 ">
                    <div class="d-flex flex-column">
                        <h3>${forum.fields.BookName}</h3>
                        <p class="">${forum.fields.username} posted on ${forum.fields.dateOfPosting}</p>
                        <p class="">${forum.fields.forumsDescription}</p>
                        <p class="">${forum.fields.userReview}</p>
                    </div>
                </td>
                <td onclick="window.location='forum/${forum.pk}/';" class="col-md-3">
                    <div class="d-flex flex-column">
                        <h5 class="text-center">Reply</h5>
                        <h5 class="text-center">${forum.fields.repliesTotal}</h5>
                    </div>
                </td>
        `;
        // Conditionally add the delete button if userRole is 'A'
        if (userRole === 'A') {
            htmlString += `
                <td>
                    <div class="display-btn">
                        <a>
                            <button type="submit" class="remove-btn" onclick="deleteForum(${forum.pk})">🗑</button>
                        </a>
                    </div>
                </td>
            `;
        }

        htmlString += `</tr>`;
    });
    
    document.getElementById("list_of_forms").innerHTML = htmlString
}

refreshForums()

function addForums() {
    fetch("add_Forum_ajax/", {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(refreshForums)

    document.getElementById("form").reset()
    return false
}

function deleteForum(forum_id) {
    fetch(`delete_Forum/${forum_id}/`, {
        method: "DELETE",
    }).then(refreshForums)
    return false
}

document.addEventListener("DOMContentLoaded", function() {
    // Initialize CKEditor for the "userReview" div
    const basicToolbar = [
    { name: 'document', items: ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates'] },
    { name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'] },
    { name: 'styles', items: ['Format', 'Font', 'FontSize'] },
    { name: 'basicstyles', items: ['Bold', 'Italic', 'RemoveFormat', 'NumberedList', 'BulletedList'] }, // Add Bold and Italic
    { name: 'insert', items: ['Image', 'Table', 'HorizontalRule'] }, // Add Image
    { name: 'links', items: ['Link', 'Unlink'] },
    { name: 'tools', items: ['Maximize', 'ShowBlocks', 'About'] },
    // Add more basic toolbar items as needed
    ];

    CKEDITOR.replace('userReview', {
        toolbar: basicToolbar,
    });


    // Function to reset CKEditor content
    function resetCKEditor() {
        if (CKEDITOR.instances.userReview) {
            CKEDITOR.instances.userReview.setData(''); // Clear CKEditor content
        }
    }

    const form = document.getElementById("form");
    
    

    // Attach the resetCKEditor function to the modal's "show" event
    document.getElementById("button_add").onclick = function() {
        const ckEditorContent = CKEDITOR.instances.userReview.getData();
        const userReviewTextarea = form.querySelector("userReview");
        userReview.value = CKEDITOR.instances.userReview.getData();
        console.log("Masuk",userReview.value)

        addForums()

        resetCKEditor()
    };
}); 

// {% comment %} document.getElementById("ForumFilter").onclick = console.log('berhasil') {% endcomment %}

const myModal = new bootstrap.Modal(document.getElementById("staticBackdrop"));

myModal._element.addEventListener('hidden.bs.modal', () => {
// Clear the form fields by resetting the form
document.getElementById("form").reset();

});