# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**MelodyAI 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

It generates a ranked list of 5 songs that best match a user's preferred genre, mood, energy, and tempo. It assumes the user has one genre and one mood they want at a time and that those preferences can be described with exact labels. This is for classroom exploration, not real users.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Each song uses six features: genre, mood, energy, tempo, valence, and danceability. The user tells the system their preferred genre, mood, energy level, tempo, and whether they like acoustic music. The system then goes through every song and gives it a score based on how well it matches. Genre and mood are worth the most points because they get full credit on an exact match. Energy, tempo, valence, and danceability are scored by how close the song's value is to what the user wants, so a song that is almost the right energy still gets most of those points. An acoustic bonus is added if the user likes acoustic music and the song is highly acoustic. All the points are added up and the top 5 songs are returned.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 20 songs. Genres include lofi, edm, blues, pop, rock, jazz, ambient, soul, latin, folk, classical, synthwave, indie pop, hip-hop, country, metal, and r&b. Moods include happy, chill, energetic, sad, intense, focused, relaxed, moody, romantic, and melancholic. 10 songs were added to the original starter dataset. Most genres still only have one song, so users with niche taste have very little variety to choose from. Musical taste that blends genres, like someone who enjoys the energy of EDM but the tone of blues, is not well represented.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users with a single clear genre and mood preference. The Chill/Lofi profile produced a top 5 that felt completely right, with three lofi songs at the top and calm acoustic tracks filling the rest. The scoring correctly captures how close a song's energy and tempo feel to what the user wants, so small numerical differences still produce sensible rankings. The explanation output for each recommendation also makes it easy to see exactly why a song ranked where it did.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system creates a filter bubble around genre when genre is worth more points than any other single feature. A user who prefers blues will almost always receive blues songs at the top, even when those songs score poorly on energy, tempo, and danceability. The adversarial experiment showed this clearly since a user with very high energy and fast tempo targets still received a slow blues song as their top result because the genre and mood label match outweighed every numerical signal. The catalog also only contains one song per niche genre, so a genre match locks in the top result before any comparison even begins.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

A Chill/Lofi listener, a Hype/Workout EDM listener, a Melancholic Blues listener, and an adversarial profile with conflicting preferences profile were tested. For each run, the goal was to check whether the top 5 songs matched the genre and mood of the profile. The Chill/Lofi and Melancholic profiles produced results that felt correct. The biggest surprise was in the EDM profile, where "Gym Hero", which is a pop song with an intense label, ranked second because its energy and danceability numbers were close to the EDM user even though the genre was different. The adversarial profile confirmed the system's weakness when a user asking for blues and sad songs but with high energy targets still received EDM and rock songs in the bottom half of the top 5. A weight shift experiment was also run, which doubled the energy multiplier and halved the genre bonus. The rankings stayed the same but the scores shifted.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Allowing users to set a mood range instead of one exact label would help the system serve listeners whose taste sits between two moods, like someone who wants something between chill and focused. Also, expanding the catalog to at least five songs per genre would give the scoring more meaningful options to compare and reduce the effect of a single song locking in the top spot.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Tuning weights is harder than it looks because changing one value shifts the entire balance of the scoring, and a weight that feels right for one profile can make results worse for another. The most unexpected discovery was that doubling the energy weight did not change the ranking order at all, which showed that the overall structure of the scoring mattered more than any single weight. This changed how I think about apps like Spotify because it makes me wonder how many labels they track for each song and how they go about tuning all of them.
