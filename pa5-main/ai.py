from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        self.conflict = False

    def solve(self, problem):
        sigma = {} #dictionary
        domains = init_domains()
        restrict_domain(domains, problem)
        decision = [] #list

        while True:
            sigma, domains = self.propagate(sigma, domains)
            if not self.conflict:
                if len(sigma) == len(sd_spots):
                    for x in sigma:
                        sigma[x] = [sigma[x]]
                    return sigma
                else:
                    sigma, x = self.makeDecision(sigma, domains)
                    decision.append((copy.deepcopy(sigma), x, copy.deepcopy(domains)))
            else:
                if len(decision) == 0:
                    return None
                else:
                    self.conflict = False
                    sigma, domains = self.backtrack(decision)

    def propagate(self, sigma, domains):
        while True:
            arc_consistent = True
            for x in sd_spots:
                if x not in sigma and len(domains[x]) == 1:
                    sigma[x] = domains[x][0]
                if x in sigma and len(domains[x]) > 1:
                    domains[x] = [sigma[x]]
                if len(domains[x]) == 0:
                    self.conflict = True
                    return sigma, domains
                
                #arc_consistent = True
                for x2 in sd_peers[x]: #x1 and x2 are peers
                    if len(domains[x2]) == 1: #D(x2) only has one element
                        element = domains[x2][0]
                        if element in domains[x]: #D(x1) contains that element
                            arc_consistent = False
                            domains[x].remove(element)
                            break
            if arc_consistent:
                return sigma, domains
                
    def makeDecision(self, sigma, domains):
        for x in sd_spots:
            if domains[x] and x not in sigma:
                sigma[x] = domains[x][0]
                return sigma, x
        return None, None
            
    def backtrack(self, decision):
        sigma, x, domains = decision.pop()
        a = sigma[x]
        del sigma[x]
        domains[x].remove(a)
        return sigma, domains


    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F sigmas solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, sigmas):
        # TODO: decode 'sigmas' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
