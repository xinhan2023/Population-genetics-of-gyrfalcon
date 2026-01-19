import pandas as pd


def get_positions(file):
    num = 10000
    F = pd.read_table(file, sep="\t", header=None)

    results = []
    for chrom, group in F.groupby(0):
        positions = group[1].sort_values().values
        selected_positions = [positions[0]]
        print(f'{positions}\t{selected_positions}')
        print(positions[1:])
        for pos in positions[1:]:
            if pos - selected_positions[-1] >= num:
                # print(f'{pos}\t{selected_positions}')
                selected_positions.append(pos)

        results.append((chrom, selected_positions))

    return results


def write_results(results):
    with open(f"POS.bed", 'w') as f:
        for chrom, positions in results:
            for pos in positions:
                f.write(f"{chrom}\t{pos}\n")


results = get_positions('pos.txt')
write_results(results)
