import seaborn as sns
import matplotlib.pyplot as plt

def show_correlation_matrix(df):
    corr_matrix = df.corr(numeric_only=True)

    plt.figure(figsize=(12, 10))
    sns.set(font_scale=1.1)
    sns.set_style("white")

    heatmap = sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )

    plt.title("Matrice di Correlazione delle Feature", fontsize=16, pad=15)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()