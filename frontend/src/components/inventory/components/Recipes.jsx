import React, {useState} from 'react'

const Recipes = () => {
	const [recipes, setRecipes] = useState([]);
	const [loading, setLoading] = useState(false);

	const makeRecipe = async () => {
		console.log("makeRecipe triggered!");
		setLoading(true);
		try{
			console.log("Fetching /recipe...");
			const Recipe = await fetch('/recipe');
			console.log(Recipe);
			console.log(Recipe.json());
			const preOutput = await Recipe.json();
			console.log(preOutput);

			if(preOutput.error){
				alert(preOutput.error);
				setLoading(false);
				return;
			}
			console.log(preOutput);
			console.log(preOutput.prompt);
			const aiResponse = await fetch(`https://weathered-frog-de80.vaibhavpanchanadam.workers.dev/?prompt=${preOutput.prompt}`);
			console.log(aiResponse);
			const output = await aiResponse.json();
			console.log(output);
			setRecipes(output);
			return output;
		} catch(err){
			console.log("Error generating recipe- please try again");
		}
		setLoading(false);
	}
	return(
		<div>
			<button onClick={makeRecipe} disabled={loading}> {loading ? 'Generating Recipes...' : 'Get Recipes'}
				</button> 

				{recipes && (
                <div>
                    <h2>Generated Recipes</h2>
                    <pre>{recipes}</pre>
                </div>
            )}
        </div>
    );


};

export default Recipes
