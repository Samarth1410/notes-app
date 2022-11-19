// this function takes noteId as input and redirects the delete command to delete-note route
// this is a standard way to do it
function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }