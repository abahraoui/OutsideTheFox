import ast


class UserExecutionVisitor(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node.func, ast.Name):
            print(node.func.id)
        ast.NodeVisitor.visit(self, node)
