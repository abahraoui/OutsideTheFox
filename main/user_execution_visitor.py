import ast


class UserExecutionVisitor(ast.NodeTransformer):
    def visit(self, node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.value.id == "sys":
            return ast.Pass()

        child = ast.NodeTransformer.visit(self, node)

        if isinstance(child, ast.Pass):
            return ast.Pass()
        else:
            return child


