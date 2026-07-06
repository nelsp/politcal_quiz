#!/usr/bin/env python3
"""
Philosophical Leanings Quiz
============================
A 90-question survey across 30 dimensions (15 opposing pairs).

Modes:
  --interactive              Original terminal-based quiz
  --agent "Name"             AI-agent mode: prints questions, reads scores from stdin
  --batch "Name1,Name2,..."  Batch mode for multiple thinkers (agent-answered via stdin)
  --analyze results/         Generate comparison outputs from saved JSON results
  --demo                     Print all questions with dimension labels (no answering)

AI Agent Usage:
  Upload this file and give the agent this prompt:

  "You are an expert in philosophy, literature, theology, and political science.
   Run this script in agent mode for each person in the list. For each question,
   respond with a single integer from 1 (strongly disagree) to 10 (strongly agree)
   based on the known writings, teachings, and philosophical positions of that person.
   Save all charts and results. Then run --analyze to generate comparisons."
"""

import argparse
import json
import os
import random
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Questions: each dimension has exactly 3 questions
# ---------------------------------------------------------------------------
QUESTIONS = {
"Spiritual": [
"A spiritual view of reality enriches life by recognizing a profound, non-physical essence, such as a soul or divine purpose, that gives meaning and connection beyond the material world. (Spiritual = existence of a non-physical soul, spirit, or divine essence)",
"There exists a spiritual dimension to reality that transcends the purely physical world.",
"Recognizing a spiritual reality opens us to deeper experiences of love, purpose, and transcendence that enrich every aspect of human existence."
],
"Material": [
"A material view of reality empowers us by focusing on the tangible, scientific world of matter and energy, providing clear, evidence-based understanding and practical solutions. (Material = reality consists only of physical matter and energy)",
"Reality consists only of physical matter and energy that can be measured and studied scientifically.",
"Grounding ourselves in the material world of science and observable reality equips us with powerful tools to solve problems and enhance quality of life for all."
],
"Voluntary Actions": [
"Embracing voluntary actions fosters a society of mutual respect and prosperity, where individuals freely exchange and cooperate without force. (Voluntary actions = choices made freely without compulsion or threat)",
"Human progress thrives when actions are undertaken willingly, driven by personal consent and agreement.",
"Prioritizing voluntary interactions builds trust, innovation, and harmony in communities, allowing each person to pursue their own path unhindered."
],
"Coercion": [
"Utilizing coercion ensures order and stability in society by compelling compliance where voluntary agreement fails. (Coercion = use of force or threat to influence behavior against one's will)",
"Social structures often require coercive measures to maintain authority and prevent chaos.",
"Applying coercion strategically can align individual actions with collective goals, securing the greater good even at the cost of personal freedoms."
],
"Free Will": [
"Affirming free will empowers individuals to shape their destinies through conscious choices, unbound by predetermined paths. (Free Will = the ability to make choices independent of deterministic causes)",
"Human existence gains authenticity when we recognize our capacity for uncaused, self-determined decisions.",
"Celebrating free will inspires moral responsibility and personal growth, as each action reflects our true intentions and values."
],
"Determinism": [
"Embracing determinism provides a scientific framework for understanding behavior as the inevitable outcome of prior causes. (Determinism = all events, including human actions, are determined by preceding causes)",
"Reality unfolds through a chain of causal necessities, leaving no room for uncaused choices.",
"Accepting determinism enhances predictive power in psychology and society, allowing for better interventions based on causal laws."
],
"Teleological": [
"A teleological approach guides ethics by focusing on outcomes and purposes, promoting actions that maximize happiness and fulfillment. (Teleological = ethics based on consequences and ends rather than rules)",
"Moral decisions should aim toward achieving the greatest good or desired ends.",
"Pursuing teleological principles fosters a pragmatic morality that adapts to real-world results, enhancing overall well-being."
],
"Deontological": [
"A deontological framework upholds moral integrity by adhering to universal duties and rules, regardless of outcomes. (Deontological = ethics based on rules and duties rather than consequences)",
"Right actions are defined by adherence to principles and obligations, not by their results.",
"Emphasizing deontological ethics builds a foundation of justice and respect for persons, ensuring consistent moral behavior."
],
"Individualism": [
"Championing individualism unleashes personal potential by prioritizing self-reliance and individual rights over group demands. (Individualism = emphasis on individual autonomy and self-interest)",
"Society flourishes when individuals pursue their own goals freely, without subordination to collectives.",
"Valuing individualism cultivates innovation, creativity, and personal achievement, leading to a dynamic and prosperous world."
],
"Collectivism": [
"Advocating collectivism strengthens community bonds by subordinating individual interests to the welfare of the group. (Collectivism = emphasis on group goals and communal ownership over individual pursuits)",
"True progress arises from collective efforts and shared responsibilities.",
"Embracing collectivism promotes solidarity, equality, and mutual support, creating a more harmonious and equitable society."
],
"Optimism": [
"An optimistic outlook inspires hope and progress by viewing the world as inherently good and improvable. (Optimism = belief in positive outcomes and the benevolence of existence)",
"Life's challenges are opportunities for growth in a fundamentally rational and benevolent universe.",
"Fostering optimism motivates action and resilience, leading to advancements and a brighter future for humanity."
],
"Nihilism": [
"Embracing nihilism liberates by rejecting inherent meaning, allowing individuals to create their own values amid absurdity. (Nihilism = denial of objective meaning, truth, or values)",
"Existence lacks intrinsic purpose, rendering traditional values illusory.",
"Confronting nihilism encourages authentic living and self-defined purpose, free from false illusions."
],
"Objective": [
"An objective perspective grounds knowledge in universal truths independent of personal opinions. (Objective = existence of absolute, mind-independent truths)",
"Reality possesses inherent structures and truths that can be discovered rationally.",
"Pursuing objective understanding fosters reliable knowledge and ethical standards applicable to all."
],
"Relative": [
"A relative viewpoint enriches diversity by seeing truths as dependent on contexts, cultures, or perspectives. (Relative = truths and values are subjective or context-dependent)",
"Knowledge and morality vary according to individual or societal frameworks.",
"Accepting relativity promotes tolerance and adaptability in a multifaceted world."
],
"Change": [
"Embracing change drives evolution and progress by recognizing flux as the essence of reality. (Change = constant transformation and adaptation)",
"All things are in perpetual motion, necessitating continual renewal.",
"Welcoming change sparks innovation and societal advancement, adapting to new realities."
],
"Tradition": [
"Upholding tradition preserves wisdom and stability by drawing on time-tested practices and values. (Tradition = adherence to established customs and heritage)",
"Societal order relies on continuity with the past and inherited norms.",
"Valuing tradition fosters cultural continuity and moral guidance across generations."
],
"Theism": [
"Affirming theism provides profound purpose through belief in a divine creator and transcendent order. (Theism = belief in a personal God or gods)",
"A supreme being governs the universe with intention and moral law.",
"Embracing theism offers spiritual fulfillment and ethical direction rooted in divine will."
],
"Atheism": [
"Embracing atheism empowers human reason by rejecting supernatural explanations for natural phenomena. (Atheism = disbelief in gods or supernatural beings)",
"The universe operates without divine intervention, explainable through science.",
"Promoting atheism encourages self-reliance and evidence-based understanding of existence."
],
"Equality": [
"Advocating equality ensures justice by treating all individuals as deserving of equal rights and opportunities. (Equality = sameness in status, rights, and opportunities)",
"Social systems should minimize disparities to achieve fairness.",
"Pursuing equality builds inclusive societies where everyone can thrive without privilege barriers."
],
"Natural Differences": [
"Recognizing natural differences honors diversity by acknowledging inherent variations in abilities and roles. (Natural Differences = innate variations among individuals or groups)",
"Humanity's strengths lie in biological and hierarchical distinctions.",
"Embracing natural differences promotes realistic social structures and merit-based progress."
],
"Reason": [
"Prioritizing reason illuminates truth through logical analysis and deduction, independent of sensory distortions. (Reason = reliance on logic and intellect over feelings)",
"Knowledge derives from rational faculties and innate ideas.",
"Cultivating reason advances philosophy, science, and ethical decision-making."
],
"Emotion": [
"Valuing emotion enriches understanding by viewing passions as the foundation of motivation and morality. (Emotion = reliance on feelings and sentiments over pure logic)",
"Human actions stem from affective impulses rather than abstract reason.",
"Harnessing emotion fosters empathy, creativity, and authentic human connections."
],
"Nature": [
"Emphasizing nature highlights innate biological factors shaping behavior and traits. (Nature = innate, genetic influences on development)",
"Human characteristics are largely determined by heredity and evolution.",
"Understanding nature informs psychology and policy with evidence-based insights."
],
"Nurture": [
"Stressing nurture empowers change by focusing on environmental influences in shaping individuals. (Nurture = environmental and experiential influences on development)",
"Behavior and identity are molded by upbringing and experiences.",
"Prioritizing nurture enables educational and social reforms for personal growth."
],
"Absolutism": [
"Upholding absolutism ensures moral clarity through unchanging principles and truths. (Absolutism = belief in fixed, universal standards)",
"Ethical and political authority derives from absolute rules or sovereign power.",
"Adhering to absolutism provides steadfast guidance in governance and ethics."
],
"Pragmatism": [
"Embracing pragmatism adapts effectively by evaluating ideas based on practical consequences. (Pragmatism = truth defined by usefulness and outcomes)",
"Knowledge evolves through experimentation and real-world application.",
"Applying pragmatism solves problems dynamically, fostering progress and flexibility."
],
"Safety": [
"Prioritizing safety builds secure societies by minimizing threats through structured authority and protections. (Safety = emphasis on security and risk avoidance)",
"Human well-being requires safeguards against uncertainty and harm.",
"Focusing on safety promotes stability, welfare, and collective peace."
],
"Risk": [
"Embracing risk fuels innovation by accepting uncertainty as a catalyst for growth and achievement. (Risk = willingness to engage with uncertainty for potential gains)",
"Progress demands venturing beyond security into creative destruction.",
"Valuing risk encourages boldness, entrepreneurship, and evolutionary advancement."
],
"Rational Self-Interest": [
"Pursuing rational self-interest drives prosperity by aligning actions with personal benefit and voluntary exchange. (Rational Self-Interest = calculated pursuit of one's own advantage)",
"Individual flourishing stems from enlightened egoism and market dynamics.",
"Championing rational self-interest generates wealth, liberty, and societal harmony."
],
"Altruism": [
"Advocating altruism enhances humanity by prioritizing others' welfare over personal gain. (Altruism = selfless concern for the well-being of others)",
"Moral duty involves sacrificing for the greater good or universal benevolence.",
"Practicing altruism fosters compassion, equity, and ethical progress in society."
]
}

# The 15 opposing pairs (left ↔ right on the radar chart)
OPPOSING_PAIRS = [
    ("Spiritual", "Material"),
    ("Voluntary Actions", "Coercion"),
    ("Free Will", "Determinism"),
    ("Teleological", "Deontological"),
    ("Individualism", "Collectivism"),
    ("Optimism", "Nihilism"),
    ("Objective", "Relative"),
    ("Change", "Tradition"),
    ("Theism", "Atheism"),
    ("Equality", "Natural Differences"),
    ("Reason", "Emotion"),
    ("Nature", "Nurture"),
    ("Absolutism", "Pragmatism"),
    ("Safety", "Risk"),
    ("Rational Self-Interest", "Altruism"),
]


# Radar chart ordering: opposing pairs placed on opposite sides
PAIR_ORDER = [
    "Spiritual", "Objective", "Voluntary Actions", "Free Will", "Teleological",
    "Individualism", "Optimism", "Change", "Atheism", "Natural Differences",
    "Reason", "Rational Self-Interest", "Nature", "Absolutism", "Safety",
    "Material", "Relative", "Coercion", "Determinism", "Deontological",
    "Collectivism", "Nihilism", "Tradition", "Theism", "Equality",
    "Emotion", "Altruism", "Nurture", "Pragmatism", "Risk"
]


# ---------------------------------------------------------------------------
# Core quiz engine
# ---------------------------------------------------------------------------

def build_question_list(shuffle=False, seed=None):
    """Return list of (dimension, question_index, question_text) tuples."""
    qlist = []
    for dim, qs in QUESTIONS.items():
        for idx, q in enumerate(qs):
            qlist.append((dim, idx, q))
    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(qlist)
    return qlist


def run_quiz(answerer_fn, person_name="Anonymous", shuffle=False, seed=42):
    """
    Run the full 90-question quiz.

    Parameters
    ----------
    answerer_fn : callable
        Signature: (question_number: int, total: int, dimension: str, question: str, question_index: int) -> int
        Must return an integer 1-10.
    person_name : str
        Name for labeling outputs.
    shuffle : bool
        Whether to shuffle question order.
    seed : int
        Random seed for reproducible shuffling.

    Returns
    -------
    dict with keys:
        'person': str
        'raw_responses': list of dicts with dimension, question_index, question, score
        'dimension_scores': dict of dimension -> average score
    """
    qlist = build_question_list(shuffle=shuffle, seed=seed)
    raw_responses = []
    dim_totals = {d: 0 for d in QUESTIONS}
    dim_counts = {d: 0 for d in QUESTIONS}

    for i, (dim, qidx, qtext) in enumerate(qlist):
        score = answerer_fn(i + 1, len(qlist), dim, qtext, qidx)
        score = max(1, min(10, int(score)))
        raw_responses.append({
            "dimension": dim,
            "question_index": qidx,
            "question": qtext,
            "score": score
        })
        dim_totals[dim] += score
        dim_counts[dim] += 1

    dimension_scores = {}
    for dim in QUESTIONS:
        if dim_counts[dim] > 0:
            dimension_scores[dim] = dim_totals[dim] / dim_counts[dim]
        else:
            dimension_scores[dim] = 0

    return {
        "person": person_name,
        "raw_responses": raw_responses,
        "dimension_scores": dimension_scores
    }


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

def generate_radar_chart(dimension_scores, person_name, output_path):
    """Generate and save a radar chart for a single person."""
    angles = np.linspace(0, 2 * np.pi, len(PAIR_ORDER), endpoint=False)
    stats = [dimension_scores.get(dim, 0) for dim in PAIR_ORDER]

    angles_closed = np.concatenate([angles, [angles[0]]])
    stats_closed = stats + [stats[0]]

    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles_closed, stats_closed, 'o-', linewidth=2)
    ax.fill(angles_closed, stats_closed, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles), PAIR_ORDER, fontsize=8)
    ax.set_ylim(0, 10)
    ax.set_title(f"Philosophical Leanings: {person_name}", va='bottom', pad=30, fontsize=14)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if np.isclose(angle, 0) or np.isclose(angle, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    ax.set_rlabel_position(30)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved radar chart: {output_path}")


def generate_overlay_chart(all_results, output_path):
    """Generate a single radar chart with all thinkers overlaid."""
    angles = np.linspace(0, 2 * np.pi, len(PAIR_ORDER), endpoint=False)
    angles_closed = np.concatenate([angles, [angles[0]]])

    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111, polar=True)

    colors = plt.cm.tab10(np.linspace(0, 1, len(all_results)))

    for result, color in zip(all_results, colors):
        scores = result["dimension_scores"]
        stats = [scores.get(dim, 0) for dim in PAIR_ORDER]
        stats_closed = stats + [stats[0]]
        ax.plot(angles_closed, stats_closed, 'o-', linewidth=2, label=result["person"], color=color)
        ax.fill(angles_closed, stats_closed, alpha=0.08, color=color)

    ax.set_thetagrids(np.degrees(angles), PAIR_ORDER, fontsize=8)
    ax.set_ylim(0, 10)
    ax.set_title("Philosophical Leanings: All Thinkers Compared", va='bottom', pad=30, fontsize=14)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if np.isclose(angle, 0) or np.isclose(angle, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    ax.set_rlabel_position(30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved overlay chart: {output_path}")


def generate_heatmap(all_results, output_path):
    """Generate a heatmap of thinkers × dimensions."""
    import pandas as pd
    import seaborn as sns

    names = [r["person"] for r in all_results]
    data = []
    for r in all_results:
        row = [r["dimension_scores"].get(dim, 0) for dim in PAIR_ORDER]
        data.append(row)

    df = pd.DataFrame(data, index=names, columns=PAIR_ORDER)

    fig, ax = plt.subplots(figsize=(22, max(6, len(names) * 1.2)))
    sns.heatmap(df, annot=True, fmt=".1f", cmap="RdYlGn", vmin=1, vmax=10,
                linewidths=0.5, ax=ax, cbar_kws={"label": "Score (1-10)"})
    ax.set_title("Philosophical Leanings Heatmap", fontsize=14, pad=15)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved heatmap: {output_path}")


# ---------------------------------------------------------------------------
# Analysis / comparison
# ---------------------------------------------------------------------------

def generate_comparison_matrix(all_results, output_path):
    """Save a CSV matrix of thinkers × dimension scores."""
    import pandas as pd

    names = [r["person"] for r in all_results]
    data = {}
    for r in all_results:
        data[r["person"]] = {dim: r["dimension_scores"].get(dim, 0) for dim in PAIR_ORDER}

    df = pd.DataFrame(data).T
    df.index.name = "Thinker"
    df = df[PAIR_ORDER]
    df.to_csv(output_path)
    print(f"  Saved comparison matrix: {output_path}")
    return df


def generate_pairwise_distances(all_results, output_path):
    """Compute and save pairwise Euclidean distances between thinkers."""
    import pandas as pd
    from scipy.spatial.distance import pdist, squareform

    names = [r["person"] for r in all_results]
    vectors = []
    for r in all_results:
        vectors.append([r["dimension_scores"].get(dim, 0) for dim in PAIR_ORDER])

    dist_matrix = squareform(pdist(vectors, metric='euclidean'))
    df = pd.DataFrame(dist_matrix, index=names, columns=names)
    df.index.name = "Thinker"
    df.to_csv(output_path)
    print(f"  Saved pairwise distances: {output_path}")

    # Also print to console
    print("\n  Pairwise Euclidean Distances:")
    print(df.round(2).to_string())
    return df


def generate_pair_difference_table(all_results, output_path):
    """
    For each opposing pair, show each thinker's score on both sides
    and the net leaning. Saves as CSV.
    """
    import pandas as pd

    rows = []
    for r in all_results:
        for left, right in OPPOSING_PAIRS:
            l_score = r["dimension_scores"].get(left, 0)
            r_score = r["dimension_scores"].get(right, 0)
            net = l_score - r_score
            if net > 0:
                leaning = f"{left} (+{net:.1f})"
            elif net < 0:
                leaning = f"{right} (+{abs(net):.1f})"
            else:
                leaning = "Neutral"
            rows.append({
                "Thinker": r["person"],
                "Pair": f"{left} ↔ {right}",
                left: round(l_score, 1),
                right: round(r_score, 1),
                "Net": round(net, 1),
                "Leaning": leaning
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"  Saved pair differences: {output_path}")
    return df


# ---------------------------------------------------------------------------
# Answerer functions for different modes
# ---------------------------------------------------------------------------

def interactive_answerer(q_num, total, dimension, question, question_index=0):
    """Terminal-based interactive answerer (original behavior)."""
    print(f"\nQuestion {q_num} of {total}")
    print(f"\n{question}")
    response = input("Please enter a number from 1 to 10 (1=strongly disagree, 10=strongly agree): ")
    while not response.strip().isdigit() or not 1 <= int(response.strip()) <= 10:
        response = input("Invalid input. Please enter a number from 1 to 10: ")
    return int(response.strip())


def stdin_answerer(q_num, total, dimension, question, question_index=0):
    """
    Agent-compatible answerer: prints question to stdout, reads score from stdin.
    Designed for AI agents that can interact with running programs.
    """
    print(f"\n[Question {q_num}/{total}] [{dimension}]")
    print(question)
    print("Score (1-10): ", end="", flush=True)
    response = input()
    try:
        val = int(response.strip())
        if 1 <= val <= 10:
            return val
    except ValueError:
        pass
    print(f"  (Invalid input '{response}', defaulting to 5)")
    return 5


def dict_answerer(scores_dict):
    """
    Create an answerer from a pre-built dictionary.

    Parameters
    ----------
    scores_dict : dict
        Mapping of dimension -> score (int 1-10).
        All questions in that dimension get the same score.
        OR mapping of (dimension, question_index) -> score for per-question control.

    Returns
    -------
    callable suitable for run_quiz().
    """
    def _answer(q_num, total, dimension, question, question_index=0):
        # Try per-question lookup first: (dimension, question_index)
        if (dimension, question_index) in scores_dict:
            return scores_dict[(dimension, question_index)]
        # Fall back to dimension-level
        return scores_dict.get(dimension, 5)
    return _answer


# ---------------------------------------------------------------------------
# Save / load results
# ---------------------------------------------------------------------------

def save_results(result, output_dir):
    """Save quiz results as JSON."""
    os.makedirs(output_dir, exist_ok=True)
    safe_name = result["person"].replace(" ", "_")
    path = os.path.join(output_dir, f"{safe_name}_results.json")
    with open(path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Saved results: {path}")
    return path


def load_results(json_path):
    """Load quiz results from JSON."""
    with open(json_path, 'r') as f:
        return json.load(f)


def load_all_results(results_dir):
    """Load all JSON result files from a directory."""
    results = []
    for fname in sorted(os.listdir(results_dir)):
        if fname.endswith("_results.json"):
            path = os.path.join(results_dir, fname)
            results.append(load_results(path))
    return results


# ---------------------------------------------------------------------------
# High-level workflows
# ---------------------------------------------------------------------------

def run_interactive(output_dir="results"):
    """Run the quiz interactively in terminal."""
    name = input("Enter your name: ").strip() or "Anonymous"
    result = run_quiz(interactive_answerer, person_name=name, shuffle=True)
    os.makedirs(output_dir, exist_ok=True)
    save_results(result, output_dir)
    safe_name = name.replace(" ", "_")
    chart_path = os.path.join(output_dir, f"{safe_name}_phil_chart.png")
    generate_radar_chart(result["dimension_scores"], name, chart_path)
    print(f"\nDone! Results saved to {output_dir}/")
    return result


def run_agent(person_name, output_dir="results"):
    """Run the quiz in agent mode (stdin/stdout for AI agent interaction)."""
    print(f"\n{'='*70}")
    print(f"PHILOSOPHICAL LEANINGS QUIZ")
    print(f"{'='*70}")
    print(f"\nYou are answering as: {person_name}")
    print(f"For each question, enter a score from 1 (strongly disagree) to 10 (strongly agree).")
    print(f"Answer as {person_name} would, based on their known philosophical positions.\n")

    result = run_quiz(stdin_answerer, person_name=person_name, shuffle=False)
    os.makedirs(output_dir, exist_ok=True)
    save_results(result, output_dir)
    safe_name = person_name.replace(" ", "_")
    chart_path = os.path.join(output_dir, f"{safe_name}_phil_chart.png")
    generate_radar_chart(result["dimension_scores"], person_name, chart_path)
    return result


def run_batch_agent(thinker_names, output_dir="results"):
    """Run the quiz for multiple thinkers via stdin agent mode."""
    all_results = []
    for name in thinker_names:
        print(f"\n{'#'*70}")
        print(f"# NOW ANSWERING AS: {name}")
        print(f"{'#'*70}")
        result = run_agent(name, output_dir)
        all_results.append(result)
        print(f"\nCompleted quiz for {name}.\n")

    # Generate comparisons
    run_analysis(output_dir, all_results)
    return all_results


def run_from_dicts(thinker_scores, output_dir="results"):
    """
    Run the quiz for multiple thinkers using pre-built score dictionaries.
    This is the easiest mode for an AI agent that can edit/run Python directly.

    Parameters
    ----------
    thinker_scores : dict
        Mapping of person_name -> {dimension: score} dict.
        Example: {"Aristotle": {"Spiritual": 7, "Material": 4, ...}, ...}
    output_dir : str
        Directory for saving results.
    """
    all_results = []
    os.makedirs(output_dir, exist_ok=True)

    for person_name, scores_dict in thinker_scores.items():
        print(f"\nProcessing: {person_name}")
        answerer = dict_answerer(scores_dict)
        result = run_quiz(answerer, person_name=person_name, shuffle=False)
        save_results(result, output_dir)
        safe_name = person_name.replace(" ", "_")
        chart_path = os.path.join(output_dir, f"{safe_name}_phil_chart.png")
        generate_radar_chart(result["dimension_scores"], person_name, chart_path)
        all_results.append(result)

    # Generate comparisons
    run_analysis(output_dir, all_results)
    return all_results


def run_analysis(results_dir, all_results=None):
    """Generate all comparison outputs from saved or provided results."""
    if all_results is None:
        all_results = load_all_results(results_dir)

    if len(all_results) == 0:
        print("No results found to analyze.")
        return

    print(f"\n{'='*70}")
    print(f"GENERATING COMPARISON ANALYSIS FOR {len(all_results)} THINKERS")
    print(f"{'='*70}")

    os.makedirs(results_dir, exist_ok=True)

    generate_comparison_matrix(all_results, os.path.join(results_dir, "comparison_matrix.csv"))
    generate_pairwise_distances(all_results, os.path.join(results_dir, "pairwise_distances.csv"))
    generate_pair_difference_table(all_results, os.path.join(results_dir, "pair_differences.csv"))

    if len(all_results) >= 2:
        generate_overlay_chart(all_results, os.path.join(results_dir, "all_thinkers_overlay.png"))

    generate_heatmap(all_results, os.path.join(results_dir, "scores_heatmap.png"))

    print(f"\nAll analysis outputs saved to {results_dir}/")


def print_all_questions():
    """Print all 90 questions with dimension labels (for reference/demo)."""
    qlist = build_question_list(shuffle=False)
    for i, (dim, qidx, qtext) in enumerate(qlist):
        print(f"\n[Q{i+1}] [{dim}] (question {qidx+1} of 3)")
        print(f"  {qtext}")
    print(f"\nTotal: {len(qlist)} questions across {len(QUESTIONS)} dimensions")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Philosophical Leanings Quiz - Multiple modes for interactive, AI agent, and analysis use.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python phil_quiz.py --interactive
  python phil_quiz.py --agent "Aristotle"
  python phil_quiz.py --batch "Jesus,John Rawls,Aristotle,Ayn Rand"
  python phil_quiz.py --analyze results/
  python phil_quiz.py --demo
        """
    )
    parser.add_argument("--interactive", action="store_true",
                        help="Run quiz interactively in terminal")
    parser.add_argument("--agent", type=str, metavar="NAME",
                        help="Run quiz for a single thinker via stdin/stdout")
    parser.add_argument("--batch", type=str, metavar="NAMES",
                        help="Comma-separated list of thinker names for batch agent mode")
    parser.add_argument("--analyze", type=str, metavar="DIR",
                        help="Generate comparison analysis from saved results in DIR")
    parser.add_argument("--demo", action="store_true",
                        help="Print all 90 questions (no answering)")
    parser.add_argument("--output", type=str, default="results",
                        help="Output directory (default: results/)")

    args = parser.parse_args()

    if args.demo:
        print_all_questions()
    elif args.interactive:
        run_interactive(args.output)
    elif args.agent:
        run_agent(args.agent.strip(), args.output)
    elif args.batch:
        names = [n.strip() for n in args.batch.split(",") if n.strip()]
        run_batch_agent(names, args.output)
    elif args.analyze:
        run_analysis(args.analyze)
    else:
        # Default: print usage and the AI agent prompt template
        parser.print_help()
        print("\n" + "="*70)
        print("AI AGENT PROMPT TEMPLATE")
        print("="*70)
        print("""
Upload this file to an AI agent and use this prompt:

\"You are an expert in philosophy, literature, theology, history and political science.
Run phil_quiz.py using the run_from_dicts() function. For each person in the list
below, provide scores (1-10) for all questions for each of the 30 dimensions based on their known writings,
teachings, and philosophical positions. 1 = strongly disagree, 10 = strongly agree.

Thinkers: 
    "Karl Marx",
    "Friedrich Engels",
    "Vladimir Lenin",
    "Rosa Luxemburg",
    "Antonio Gramsci",
    "Edmund Burke",
    "Joseph de Maistre",
    "Giovanni Gentile",
    "Carl Schmitt",
    "Julius Evola"
 



After generating all results, the script will automatically produce:
- Individual radar charts for each thinker
- An overlay chart comparing all thinkers
- A comparison matrix CSV
- A pairwise distance matrix
- A scores heatmap

Example usage in Python:

    from phil_quiz import run_from_dicts

    thinker_scores = {
        "Jesus": {
            "Spiritual": 10, "Material": 2, "Voluntary Actions": 8, "Coercion": 3,
            "Free Will": 9, "Determinism": 2, ...  # all 30 dimensions
        },
        "Aristotle": { ... },
        ...
    }
    run_from_dicts(thinker_scores, output_dir="results")
\"
""")


if __name__ == "__main__":
    main()
