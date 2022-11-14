function deleteRecipe(recipeId) {
  fetch("/delete-recipe", {
    method: "POST",
    body: JSON.stringify({ recipeId: recipeId }),
  }).then((_res) => {
    window.location.href = "/repertoire";
  });
}
function addRecipe(recipeId) {
  fetch("/add-recipe", {
    method: "POST",
    body: JSON.stringify({ recipeId: recipeId }),
  }).then((_res) => {
    window.location.href = "/repertoire";
  });
}
