import ast

passing = ast.Pass(
    name='passing',
    args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kwarg=None, defaults=[], kw_defaults=[]),
    body=[
        ast.Pass()
    ],
    decorator_list=[],
    lineno=5,
    col_offset=0
)


class UserExecutionVisitor(ast.NodeTransformer):
    def visit(self, node):

        # Sanitizes function calls not allowed. #TODO choose whether keep this, allowed vars already sanitise some stuff. PROBLEM: blocks array.append() for example.
        # if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.value.id != "fox":
        #     print(node.func.value.id)
        #     return passing

        # Sanitizes builtins functions exec and eval that can execute code.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and (node.func.id == "exec" or node.func.id == "eval"):
            return passing

        child = ast.NodeTransformer.visit(self, node)

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Pass):
            return passing
        if isinstance(child, ast.Pass):
            return passing
        else:
            return child
