// export default{
//     async fetch(request,env){
//         try{
//             const db = foods.db;
//             const results = await db.prepare(`SELECT name, expiration_date FROM dates ORDER BY expiration_date ASC`).all();
//             if(!results || results.length === 0 || !results.length){
//                 return new Response(JSON.stringify({error: 'No food data available for recipes'}), {status: 404, headers: {'Content-Type': 'application/json'}});
                    
//                 }


//                 const foods = results.map(row=> `${row.name}`).join(",");
//                 console.log(foods);


//                 const cloudFlareInput = { text: prompt};
//                 const clourFlareResponse = "hello";
//             } catch(err){
//                 return new Response(JSON.stringify({error: 'Inocorrect parameters, please try again.'}), {status:404, headers:{'Content-Type':'application/json'}});
//             }

//     }



// }