from flask import Flask, request, jsonify
import pickle
import ast

app = Flask(__name__)

@app.route("/api/recommender", methods=["POST"])
def recommender():
    def read_association_rules(file_path):
        association_rules = []
        code_info = []

        try:
            with open(file_path, 'r') as file:
                line_count = 0
                for line in file:
                    line_count += 1
                    if line_count <= 2:
                        code_info.append(line.strip())
                        continue
                    rule = ast.literal_eval(line.strip())
                    association_rules.append(rule)

            return code_info, association_rules

        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return [], []
        except Exception as e:
            print(f"An error occurred: {e}")
            return [], []

    def get_recommendations(input_songs, association_rules):
        recommendations = []

        for rule in association_rules:
            if set(rule[0]) <= set(input_songs):
                recommendations.append((list(rule[1]), rule[2]))

        recommendations.sort(key=lambda x: x[1], reverse=True)

        sorted_recommendations = [song for song, _ in recommendations]

        return sorted_recommendations
    
    request_data = request.get_json()
    
    input_songs = request_data.get("songs", [])

    if not input_songs:
        return jsonify({"error": "No 'songs' key found in the request data"}), 400

    association_rules_file_path = '/home/pedroribeiro/project2-pv/association_rules.txt'
    code_info,rules = read_association_rules(association_rules_file_path)

    recommendations = get_recommendations(input_songs, rules)
    version = '1.0'
    
    if recommendations:
        return jsonify({
            "version" : version,
            "run_time" : code_info[1],
            "recommendations": list(set(song for sublist in recommendations for song in sublist))})
    else:
        return jsonify({"message": f"No recommendations found for {input_songs}."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=32210)
