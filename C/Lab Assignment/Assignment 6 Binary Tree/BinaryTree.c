#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left;
    struct Node *right;
} Node;

Node* createNode(int val) {
    Node* n = malloc(sizeof(Node));
    n->data = val;
    n->left = NULL;
    n->right = NULL;
    return n;
}

Node* buildTree() { // -1 for NULL
    int val;
    scanf("%d", &val);
    if (val == -1) {
        return NULL;
    }
    Node* root = createNode(val);
    root->left = buildTree();
    root->right = buildTree();
    return root;
}

int insertAtPos(Node* root, int target, char dir, int val) {
    if (!root) {
        return 0;
    }
    if (root->data == target) {
        Node** child = (dir == 'L' || dir == 'l') ? &root->left : &root->right;
        if (*child) {
            return 0;
        }
        *child = createNode(val);
        return 1;
    }
    return insertAtPos(root->left, target, dir, val) || insertAtPos(root->right, target, dir, val);
}

Node* findDeepestParent(Node* root, Node** deepest) {
    if (!root) {
        return NULL;
    }
    if (!root->left && !root->right) {
        *deepest = root;
        return NULL;
    }
    Node *q[100];
    Node *p = NULL;
    int f = 0;
    int r = 0;
    q[r++] = root;
    while (f < r) {
        Node* cur = q[f++];
        if (cur->left) {
            p = cur;
            q[r++] = cur->left;
        }
        if (cur->right) {
            p = cur;
            q[r++] = cur->right;
        }
        *deepest = cur;
    }
    return p;
}

Node* deleteBTNode(Node* root, int key) {
    if (!root) {
        return NULL;
    }
    if (!root->left && !root->right) {
        if (root->data == key) {
            free(root);
            return NULL;
        }
        return root;
    }
    Node *q[100];
    Node *target = NULL;
    Node *last = NULL;
    int f = 0;
    int r = 0;
    q[r++] = root;
    while (f < r) {
        last = q[f++];
        if (last->data == key) {
            target = last;
        }
        if (last->left) {
            q[r++] = last->left;
        }
        if (last->right) {
            q[r++] = last->right;
        }
    }
    if (target) {
        target->data = last->data;
        Node* deepest;
        Node* parent = findDeepestParent(root, &deepest);
        if (parent) {
            if (parent->right == deepest) {
                free(parent->right);
                parent->right = NULL;
            } else {
                free(parent->left);
                parent->left = NULL;
            }
        }
    }
    return root;
}

void preorder(Node* r) {
    if (r) {
        printf("%d ", r->data);
        preorder(r->left);
        preorder(r->right);
    }
}

void inorder(Node* r) {
    if (r) {
        inorder(r->left);
        printf("%d ", r->data);
        inorder(r->right);
    }
}

void postorder(Node* r) {
    if (r) {
        postorder(r->left);
        postorder(r->right);
        printf("%d ", r->data);
    }
}

void printAllTraversals(Node* r) {
    printf("Pre-order: ");
    preorder(r);
    printf("\nIn-order: ");
    inorder(r);
    printf("\nPost-order: ");
    postorder(r);
    printf("\n");
}

int main() {
    printf("Enter nodes in pre-order (-1 for NULL): ");
    Node* root = buildTree();
    int target;
    int val;
    char dir;
    printf("Insert - parent val, direction (L/R), new val: ");
    if (scanf("%d %c %d", &target, &dir, &val) == 3) {
        insertAtPos(root, target, dir, val);
    }
    printf("Delete node value: ");
    if (scanf("%d", &val) == 1) {
        root = deleteBTNode(root, val);
    }
    printAllTraversals(root);
    return 0;
}