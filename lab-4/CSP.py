from sortedcontainers import SortedSet
from operator import eq, neg

## Global variable to keep track of the total number of consistency
## checks
total_checks=0

def first(iterable):
    """Return the first element of an iterable."""
    return next(iter(iterable))

def extend(s, var, val):
    """Copy dict s and extend it by setting var to val; return copy."""
    return {**s, var: val}

class CSP:
    """
    A CSP models a Constraint Satisfaction Problem
    domains     : a dictionary that maps each variable to its domain
    constraints : a list of constraints
    variables   : a set of variables
    var_to_constr: a variable to set of constraints dictionary
    """

    def __init__(self, domains, constraints):
        """Domains is a variable:domain dictionary
        constraints is a list of constraints
        """
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.var_to_constr = {var: set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_constr[var].add(con)

    def __str__(self):
        """String representation of CSP"""
        return str(self.domains)

    def display(self, assignment=None):
        """More detailed string representation of CSP"""
        if assignment is None:
            assignment = {}
        print(assignment)

    def consistent(self, assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                   for con in self.constraints
                   if all(v in assignment for v in con.scope))


class Constraint:
    """
    A Constraint consists of:
    scope    : a tuple of variables
    condition: a function that can applied to a tuple of values
    for the variables.
    """

    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition

    def __repr__(self):
        return self.condition.__name__ + str(self.scope)

    def holds(self, assignment):
        """Returns the value of Constraint con evaluated in assignment.

        precondition: all variables are assigned in assignment
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))


def all_diff_constraint(*values):
    """Returns True if all values are different, False otherwise"""
    return len(values) == len(set(values))

def edge_label_constraint(u,v,uv):
    """Returns True if the edge label constraint hods on an edge 
    from u to v, False otherwise"""
    return abs(u - v) == uv

def is_zero(x):
    """Returns True if variable is equal to zero"""
    return x == 0

class ACSolver:
    """Solves a CSP with arc consistency and domain splitting"""

    def __init__(self, csp):
        """a CSP solver that uses arc consistency
        * csp is the CSP to be solved
        """
        self.csp = csp

    # def check(self, D: dict, constraint: Constraint, scope: tuple, assignment: dict, index):
    #     #     for value in D[scope[index]]:
    #     #         assignment[scope[index]] = value
    #     #         if index == len(scope) - 1:
    #     #             return constraint.holds(assignment)
    #     #         else:
    #     #             return self.check(D, constraint, scope, assignment, index + 1)
    #     #     return 0

    def GAC(self, orig_domains, queue=None):
        """
        Makes this CSP arc-consistent using Generalized Arc Consistency
        orig_domains: is the original domains
        queue       : is a set of (variable,constraint) pairs
        returns the reduced domains (an arc-consistent variable:domain dictionary)
        """
        ## for each variable X: D_X = dom(X)
        D = orig_domains.copy()

        ## queue = {<X, (S, R)> : (S, R) \in C, X ∈ S}
        if queue is None:
            queue = {(var, constr) for constr in self.csp.constraints for var in constr.scope}
        ## Otherwise inherit queue from calling process
        else:
            queue = queue.copy()

        checks = 0


        ## While queue is not empty
        while queue:
            X, constr = queue.pop()
            scope: tuple = constr.scope
            Y = tuple(x for x in scope if x != X)
            D_X = set()
            for x in D[X]:
                ans, additional_checks = self.any_holds(D, constr, {X: x}, Y)
                checks += additional_checks
                if ans:
                   D_X.add(x)
            if D_X != D[X]:
                add = self.new_queue(X, constr).difference(queue)
                queue |= add
                D[X] = D_X

        return True, D, checks

    def new_queue(self, var, constr):
        """
        Returns new elements to be added to queue after assigning
        variable var in constraint constr.
        """
        ## Given a <var,constr> return all <X,C> where C != constr and var is in scope of C but not X 
        return {(nvar, nconstr) for nconstr in self.csp.var_to_constr[var]
                if nconstr != constr
                for nvar in nconstr.scope
                if nvar != var}

    def any_holds(self, domains, constr, env, other_vars, ind=0, checks=0):
        """
        Returns True if Constraint constr holds for an assignment
        that extends env with the variables in other_vars[ind:]
        env is a dictionary
        Warning: this has side effects and changes the elements of env
        """
        ## Base case: no more values to assign
        if ind == len(other_vars):
            return constr.holds(env), checks + 1
        ## Recursively call any_holds for each value in domain of
        ## other_vars[ind]
        else:
            var = other_vars[ind]
            for val in domains[var]:
                # env = dict_union(env, {var:val})  # no side effects
                env[var] = val
                holds, checks = self.any_holds(domains, constr, env, other_vars, ind + 1, checks)
                if holds:
                    return True, checks
            return False, checks

    def domain_splitting(self, domains=None, queue=None):
        """
        Return a solution to the current CSP or False if there are no solutions
        queue is the list of arcs to check
        """
        global total_checks
        if domains is None:
            domains = self.csp.domains

        ## Run generalized arc-consistency to get reduced domains
        consistency, new_domains, checks = self.GAC(domains, queue)
        print(f"GAC performed {checks} consistency checks")
        total_checks+=checks
        
        ## If this CSP is inconsistent, return False
        if not consistency:
            return False

        ## If generalized arc-consistency shrunk all the domains to size 1,
        ## return the corresponding assignment
        elif all(len(new_domains[var]) == 1 for var in domains):
            return {var: first(new_domains[var]) for var in domains}

        ## Otherwise, recursively split domains
        else:
            ## Choose a variable with domain size larger than 1
            var = first(x for x in self.csp.variables if len(new_domains[x]) > 1)

            print(f"splitting on var {var}")
            
            if var:
                ## Split domain for this var
                dom1, dom2 = partition_domain(new_domains[var])                
                new_doms1 = extend(new_domains, var, dom1) ## adds new_domains[var]=dom1
                new_doms2 = extend(new_domains, var, dom2) ## adds new_domains[var]=dom2
                queue = self.new_queue(var, None) 
                return self.domain_splitting(new_doms1, queue) or \
                       self.domain_splitting(new_doms2, queue)


def partition_domain(dom):
    """Partitions domain dom into two"""
    split = len(dom) // 2
    dom1 = set(list(dom)[:split])
    dom2 = dom - dom1
    return dom1, dom2


def ac_solver(csp):
    """Arc consistency (domain splitting interface)"""
    global total_checks
    result = ACSolver(csp).domain_splitting()
    print(f"total consistency checks: {total_checks}")
    return result



