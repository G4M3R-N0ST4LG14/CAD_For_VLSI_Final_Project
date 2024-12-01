class QuineMcCluskey:
    def __init__(self, num_variables, minterms, dont_cares):
        """
        Initialize the Quine-McCluskey algorithm.
        num_variables: Number of input variables.
        minterms: List of minterms to be simplified.
        dont_cares: List of don't-care terms (optional inputs that can be ignored in output).
        """
        self.num_variables = num_variables
        self.minterms = minterms
        self.dont_cares = dont_cares
        self.all_terms = minterms + dont_cares  # Combine minterms and don't-cares for initial processing.
        self.simplified_terms = []  # Store the final simplified terms.

    def minterms_to_binary(self, terms):
        """
        Convert terms into their binary representation, padded to the required number of variables.
        terms: List of minterms or don't-cares.
        return List of binary strings.
        """
        return [bin(term)[2:].zfill(self.num_variables) for term in terms]

    def differs_by_one_bit(self, term1, term2):
        """
        Check if two binary terms differ by exactly one bit.
        term1: First binary term.
        term2: Second binary term.
        return True if the terms differ by one bit, False otherwise.
        """
        diff_count = sum(1 for i in range(len(term1)) if term1[i] != term2[i])
        return diff_count == 1

    def combine_binary_terms(self, term1, term2):
        """
        Combine two binary terms by replacing differing bits with a dash ('-').
        term1: First binary term.
        term2: Second binary term.
        return Combined binary term with dashes in differing positions.
        """
        return ''.join([term1[i] if term1[i] == term2[i] else '-' for i in range(len(term1))])

    def covers(self, implicant, minterm):
        """
        Check if an implicant covers a given minterm.
        implicant: Binary string with '-' representing wildcards.
        minterm: Binary string representing a specific term.
        return True if the implicant covers the minterm, False otherwise.
        """
        return all(implicant[i] == '-' or implicant[i] == minterm[i] for i in range(len(minterm)))

    def simplify(self):
        """
        Simplify the Boolean function using the Quine-McCluskey algorithm.
        - Combines terms that differ by one bit to create prime implicants.
        - Builds a coverage table to ensure every minterm is covered.
        - Identifies essential prime implicants and resolves overlaps.
        """
        # Step 1: Convert all terms to binary.
        binary_terms = self.minterms_to_binary(self.all_terms)
        minterm_binaries = self.minterms_to_binary(self.minterms)

        # Step 2: Combine terms iteratively until no further combination is possible.
        terms = set(binary_terms)
        prime_implicants = set()

        while terms:
            new_terms = set()
            combined = set()
            used = set()

            for term1 in terms:
                for term2 in terms:
                    if term1 != term2 and self.differs_by_one_bit(term1, term2):
                        combined_term = self.combine_binary_terms(term1, term2)
                        combined.add(combined_term)
                        used.add(term1)
                        used.add(term2)

            # Add unused terms (prime implicants) to the prime implicants set.
            for term in terms:
                if term not in used:
                    prime_implicants.add(term)

            terms = combined

        # Step 3: Build coverage table.
        coverage_table = {}
        for minterm in minterm_binaries:
            coverage_table[minterm] = [implicant for implicant in prime_implicants if self.covers(implicant, minterm)]

        # Step 4: Find essential prime implicants.
        essential_prime_implicants = set()
        for minterm, implicants in coverage_table.items():
            if len(implicants) == 1:  # If only one implicant covers this minterm.
                essential_prime_implicants.add(implicants[0])

        # Remove minterms covered by essential implicants.
        for implicant in essential_prime_implicants:
            for minterm in list(coverage_table.keys()):
                if self.covers(implicant, minterm):
                    del coverage_table[minterm]

        # Step 5: Select additional implicants to cover remaining minterms.
        while coverage_table:
            # Select the implicant that covers the most remaining minterms.
            best_choice = max(prime_implicants, key=lambda imp: sum(self.covers(imp, m) for m in coverage_table))
            essential_prime_implicants.add(best_choice)

            # Remove minterms covered by this implicant.
            for minterm in list(coverage_table.keys()):
                if self.covers(best_choice, minterm):
                    del coverage_table[minterm]

        # Store the final simplified terms.
        self.simplified_terms = sorted(list(essential_prime_implicants))


# I/O Functions
def read_blif_file(file_path):
    """
    Read a BLIF file and extract variables, minterms, and don't-cares.
    file_path: Path to the BLIF file.
    return Number of variables, minterms, don't-cares, and variable names.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    variables = []
    minterms = []
    dont_cares = []

    for line in lines:
        line = line.strip()
        if line.startswith(".inputs"):
            variables = line.split()[1:]
        elif line.startswith(".names"):
            pass  # Skip this line as it's specific to BLIF format.
        elif line and not line.startswith("."):
            inputs, output = line.split()
            if output == "1":
                minterms.append(int(inputs, 2))
            elif output == "-":
                dont_cares.append(int(inputs, 2))

    return len(variables), minterms, dont_cares, variables


def write_pla_file(file_path, num_variables, variable_names, simplified_terms):
    """
    Write the simplified terms to a PLA file.
    file_path: Path to the PLA output file.
    num_variables: Number of input variables.
    variable_names: Names of the input variables.
    simplified_terms: List of simplified terms.
    """
    with open(file_path, 'w') as file:
        file.write(f".i {num_variables}\n")
        file.write(".o 1\n")
        file.write(f".ilb {' '.join(variable_names)}\n")
        file.write(".ob F\n")
        for term in simplified_terms:
            file.write(f"{term} 1\n")
        file.write(".e\n")


# Main Driver
def quine_mccluskey_simplify(input_file, output_file):
    """
    Simplify a Boolean function from a BLIF file and save the result in PLA format.
    input_file: Path to the BLIF input file.
    output_file: Path to the PLA output file.
    """
    num_variables, minterms, dont_cares, variable_names = read_blif_file(input_file)
    qm = QuineMcCluskey(num_variables, minterms, dont_cares)

    # Simplify the Boolean function.
    qm.simplify()

    # Write the simplified Boolean function to the output PLA file.
    write_pla_file(output_file, num_variables, variable_names, qm.simplified_terms)

# Modify here for testing:
input_file = r"Insert address for input here"
output_file = r"Insert address for output here"
quine_mccluskey_simplify(input_file, output_file)