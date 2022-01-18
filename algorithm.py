import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def fgsm(model, data, target, loss_fn, epsilon, std):
    std = std.to(device)
    epsilon = epsilon / 255 / std
    x_adv = data.detach().clone()
    x_adv.requires_grad = True
    loss = loss_fn(model(x_adv), target)
    loss.backward()
    x_adv = x_adv + epsilon * x_adv.grad.detach().sign()
    return x_adv


def ifgsm(model, data, target, loss_fn, epsilon, std):
    num_iter = 20
    x_adv = data.detach().clone()
    for i in range(num_iter):
        x_adv = fgsm(model, x_adv, target, loss_fn, epsilon / 10, std)
        x_adv = torch.min(torch.max(x_adv, data - epsilon), data + epsilon)
    return x_adv


'''
def pgd():
    return 


def cw():
    return 


def advGAN():
    return '''


def setupAlgorithm(chosenAlgorithm):
    """
            if chosenAlgorithm == 'PGD':
                return pgd
            if chosenAlgorithm == 'CW':
                return cw
            if chosenAlgorithm == 'advGAN':
                return advGAN
    """
    if chosenAlgorithm == 'FGSM':
        return fgsm, 8

    elif chosenAlgorithm == 'IFGSM':
        return ifgsm, 8

    else:
        raise Exception("其他攻击算法暂不支持! 请使用README中所述的已支持攻击算法！")
