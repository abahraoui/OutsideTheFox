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
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.value.id != "fox":
            return passing

        child = ast.NodeTransformer.visit(self, node)

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Pass):
            return passing
        if isinstance(child, ast.Pass):
            return passing
        else:
            return child
