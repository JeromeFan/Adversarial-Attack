from baseAlgorithm import BaseAlgorithm


class FGSM(BaseAlgorithm):

    def __init__(self, model, loss_fn, std):
        super(FGSM, self).__init__(model, loss_fn, std)
        self.epsilon = int(input('请输入FGSM算法所需的epsilon：'))/ 255 / self.std

    def perturb(self, data, target):

        return self.fgsm(data, target, self.epsilon)
