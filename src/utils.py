import matplotlib.pyplot as plt

def plot_support_vs_patterns(supports, pattern_counts, title=None):
    """Построить график зависимости количества паттернов от поддержки"""
    plt.figure(figsize=(10, 6))
    plt.plot(supports, pattern_counts, marker='o', linewidth=2, markersize=8)
    plt.xlabel('Минимальная поддержка (%)')
    plt.ylabel('Количество частых последовательностей')
    if title:
        plt.title(title)
    else:
        plt.title('Зависимость количества паттернов от min_sup')
    plt.grid(True, alpha=0.3)
    plt.show()

def print_table(data, headers):
    """Красиво вывести таблицу (требуется tabulate)"""
    try:
        from tabulate import tabulate
        print(tabulate(data, headers=headers, tablefmt='grid'))
    except ImportError:
        print("Установите tabulate: pip install tabulate")
        for row in data:
            print(row)
