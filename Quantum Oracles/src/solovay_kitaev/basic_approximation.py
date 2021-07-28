from numpy import array, eye
from numpy.linalg import norm

class BaseCaseQuery():
    '''
        BaseCaseQuery class
        Constructs a queryable object for the base case in Solovay-Kitaev
    '''

    def __init__(self, *gates : list, depth=3, unique=True, norm_bound=1e-5):
        '''
            __init__
            Initialiser for the BaseCaseQuery
            :: *gates : list :: List of gate as the basis for the query
            :: depth         :: Depth of the query
            :: unique        :: Are the gates unique, attempts to discard approximately identical constructions, eg XX and ZZ
            :: norm_bound    :: Norm bound distance between discarded constructions
        '''
        self.depth = depth
        self.gates = gates
        self.norm_bound = norm_bound

        self.query_structure = None
        self.generate_query_structure(unique=unique)

        

    def generate_query_structure(self, unique=True):
        '''
            generate_query_structure
            Generates an array of matricies and their decompositions
            :: unique : bool :: A flag to filter the array for unique approximations
            This flag increases the construction time but may result in a more efficient (read smaller) set of gates
            leading to performance improvements at query time.
        '''
        query_structure = []
        for approximation, construction in basic_approximation_generator(*self.gates):
 
            # Check if close approximation already exists    
            approximated = False
            if len(query_structure) > 0 or not unique: # If not unique then skip this check

                for extant_approximation, extant_construction in enumerate(query_structure):
                    # Compare Frobenius norm
                    if norm(approximation - extant_approximation) < self.norm_bound:
                        approximated = True
                        break
                    
            # Not found, insert as normal
            if not approximated:
                query_structure.append((approximation, construction))
            
        self.query_structure = query_structure


    def __call__(self, unitary : array) -> tuple:
        '''
            __call__
            Calls the query method
            :: unitary : array :: Unitary for which we want to find the base approximation
            Returns a tuple of the approximate gate along with the gates required to construct it.
        '''
        return self.query(unitary)


    def query(self, unitary : array, memory_bound=False) -> tuple:
        '''
            query
            Performs a query on the base case structure
            :: unitary : array :: Unitary for which we want to find the base approximation
            :: memory_bound    :: If the basis set is too large then it's inefficient to 
            Returns a tuple of the approximate gate along with the gates required to construct it.
        '''

        distance = float('inf')
        min_dist_approx = None
        min_dist_construction = None

        # TODO Vectorise
        for approximation, construction in self.query_structure:
            current_distance = norm(unitary - approximation, ord='fro')

            if current_distance < distance:
                distance = current_distance
                min_dist_approx = approximation
                min_dist_construction = construction

        return min_dist_approx, min_dist_construction

    
    def construct_vector_norm(self, unitary : array):
        '''
            construct_vector_norm
            Constructs a vectorised query function
            Requires refactoring of the query structure to a numpy array
            :: unitary : array :: unitary to query
            Returns a vectorised function
        '''
        def matrix_norm(matrix_a : array, matrix_b : array):
            return norm(matrix_a, matrix_b, ord='fro')
        partial_norm = partial(matrix_norm, unitary)
        vector_norm = np.vectorize(partial_norm)
        return vector_norm





def basic_approximation_generator(
        *gates, 
        depth = 3):
    '''
        basic_approximation_generator
        Enumerates through convex combinations of gates
        :: gates : list :: A list of numpy array representations of gates
        :: depth :: The depth of the enumeration
    '''
    # Dimension of operator
    # Currently probably 2; need to add combinations to single qubit gates
    if len(gates) == 0:
        raise IndexError("No gates provided to basic approximation")
    matrix_rank = gates[0].shape[0]

    # Space of all sequences
    base = len(gates)
    for i in range(base ** depth):
          
        # Convert sequence to set of gates
        integer_representation = i
        current_combination = []
    
        # Perform a basis change to the number of gates
        current_power = 1
        while integer_representation != 0:
            
            # Split on individual digits and append appropriate gate 
            current_combination.append(
                    gates[
                        int(integer_representation 
                            % (base ** current_power) 
                            // (base ** (current_power - 1))
                            )
                        ]
                    )

            integer_representation -= integer_representation % (base ** current_power)
            current_power += 1

        # There needs to be a nicer way to express this
        base_approximation = eye(matrix_rank)
    
        for gate in current_combination:
            base_approximation = gate @ base_approximation

        yield base_approximation, current_combination