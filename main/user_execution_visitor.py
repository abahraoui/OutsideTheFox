import ast

# Define a 'passing' node that represents a no-operation (pass) statement
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
    """
    A custom AST (Abstract Syntax Tree) transformer that sanitizes potentially unsafe code.

    It sanitizes the built-in functions exec and eval that can execute code. It replaces these calls with a 'pass'
    statement, effectively neutralizing them using a recursive method.
    """
    def visit(self, node):
        """
        Visit a node in the AST.

        Parameters
        ----------
        node : ast.AST
            The node to visit.

        Returns
        -------
        ast.AST
            The transformed node.
        """

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
