from jit_code_generator import *
from collections import defaultdict

class AstVisitor:
    def __init__(self):
        #self.output = open(filename, 'w')
        self.code_generator = CodeGenerator()
        #list of dicts
        self.env = [defaultdict(lambda:None)]

    def enter_scope(self, env):
        self.env.append(env)

    def exit_scope(self):
        self.env.pop()


    def visit_fun(self, fun_node):
        if fun_node.subtype == "say":
            sentences = (param.accept(self) for param in fun_node.params)
            lst = self.code_generator.generate_list(sentences)
            prtstr = "'\\n'.join(%s)" % lst
            code = self.code_generator.generate_print(prtstr)
            #self.output.write(code + '\n')

        elif fun_node.subtype == "createNode":
            #self.output.write("Node()")
            code = "Node()"
        elif fun_node.subtype == "listen":
            code = "raw_input()"
        elif fun_node.subtype == "push":
            visited_params = map(lambda node : node.accept(self), fun_node.params)
            params_str = ', '.join(visited_params)
            code = "push(%s)\n" % params_str
        elif fun_node.subtype == "pull":
            visited_params = map(lambda node : node.accept(self), fun_node.params)
            params_str = ', '.join(visited_params)
            code = "pull(%s)\n" % params_str
        elif fun_node.subtype == "save":
            visited_params = map(lambda node : node.accept(self), fun_node.params)
            params_str = ', '.join(visited_params)
            code = "save(%s)\n" % params_str
        elif fun_node.subtype == "get":
            visited_params = map(lambda node : node.accept(self), fun_node.params)
            params_str = ', '.join(visited_params)
            code = "get(%s)\n" % params_str
        elif fun_node.subtype == "import":
            visited_params = map(lambda node : node.accept(self), fun_node.params)
            params_str = ', '.join(visited_params)
            code = "import(%s)\n" % params_str
        elif fun_node.subtype == "search":
            visited_params = map(lambda node : node.accept(self), fun_node.params)
            params_str = ', '.join(visited_params)
            code = "search(%s)\n" % params_str
        else:
            code = "ERROR visit_fun\n"

        return code

    def visit_binop(self, binop_node):
        op = binop_node.op
        if (binop_node.right.type == "articleop"):
            lhs  = op = ""
        else:
            lhs = binop_node.left.accept(self).strip()
            
        rhs = binop_node.right.accept(self).strip()
        if binop_node.op == "=":
            self.env[-1][lhs] = rhs
        
        code = self.code_generator.generate_binaryOp(lhs, op, rhs)
        return code

    def visit_articleop(self, articleop_node):
        if not articleop_node: return
        
        lhs = articleop_node.left.accept(self).strip()
        rhs = articleop_node.right.accept(self).strip()
        #if articleop_node.op == "=":
        #    self.env[-1][lhs] = rhs
        
        code = self.code_generator.generate_articleOp(lhs, articleop_node.op, rhs, articleop_node.assign_to, articleop_node.list_of_things)
        
        return code

    def visit_str(self, str_node):
        return str_node.value

    def visit_list(self, list_node):
        return list_node.value


    def visit_num(self, str_node):
        return str(str_node)


    def visit_id(self, id_node):
        name = id_node.name
        current_env = self.env[-1]
        val = current_env[name]
        return name

    def visit_vardecl(self, decl_node):
        init_vals = defaultdict(lambda:None)
        init_vals['string'] =  ''
        init_vals['int'] = 0
        self.env[-1][decl_node.name] = None
        code = "%s = %s\n" % (decl_node.name, str(init_vals[decl_node.type]))
        return code

    def visit_forloop(self, for_node):
        itr = for_node.itr.accept(self)
        span = for_node.span.accept(self)
        body = map(lambda n : n.accept(self), for_node.body)
        code = self.code_generator.generate_forloop(itr, span, body)
        return code

    def visit_ifblock(self, if_node):
        ifc = if_node.if_clause.accept(self).strip()
        thc = map(lambda n : n.accept(self), if_node.then_clause)
        elc = map(lambda n : n.accept(self), if_node.else_clause)
        code = self.code_generator.generate_ifblock(ifc, thc, elc)
        return code

    def visit_astfundecl(self, fundecl_node):
        varlist = map(lambda n : n.accept(self).strip(), fundecl_node.varlist)
        fun_body = map(lambda n : n.accept(self), fundecl_node.stmtlist)
        code = self.code_generator.generate_fundecl(fundecl_node.name, varlist, fun_body)
        return code
